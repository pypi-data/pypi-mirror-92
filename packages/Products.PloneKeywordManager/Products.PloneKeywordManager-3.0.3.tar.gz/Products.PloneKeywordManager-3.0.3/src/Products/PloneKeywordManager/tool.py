# -*- coding: utf-8 -*-
# Copyright (c) 2005 gocept gmbh & co. kg
# See also LICENSE.txt
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from AccessControl.class_init import InitializeClass
from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.discussion.interfaces import IComment
from plone.dexterity.interfaces import IDexterityContent
from Products.CMFCore import permissions as CMFCorePermissions
from Products.CMFCore.indexing import processQueue
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import UniqueObject
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PloneKeywordManager import config
from Products.PloneKeywordManager.compat import to_str
from Products.PloneKeywordManager.interfaces import IPloneKeywordManager
from zope import interface

# Python imports
try:
    import Levenshtein

    USE_LEVENSHTEIN = True
except ImportError:
    import difflib

    USE_LEVENSHTEIN = False


@interface.implementer(IPloneKeywordManager)
class PloneKeywordManager(UniqueObject, SimpleItem):
    """A portal wide tool for managing keywords within Plone."""

    plone_tool = 1

    id = "portal_keyword_manager"
    meta_type = "Plone Keyword Manager Tool"
    security = ClassSecurityInfo()

    manage_options = ({"label": "Overview", "action": "manage_overview"},)

    security.declareProtected(CMFCorePermissions.ManagePortal, "manage_overview")
    manage_overview = PageTemplateFile(
        "www/explainTool", globals(), __name__="manage_overview"
    )

    def _getFullIndexList(self, indexName):
        idxs = set([indexName]).union(config.ALWAYS_REINDEX)
        return list(idxs)

    @security.protected(config.MANAGE_KEYWORDS_PERMISSION)
    def change(self, old_keywords, new_keyword, context=None, indexName="Subject"):
        """Updates all objects using the old_keywords.

        Objects using the old_keywords will be using the new_keywords
        afterwards.

        Returns the number of objects that have been updated.
        """
        # #MOD Dynamic field getting
        query = {indexName: old_keywords}
        if context is not None:
            query["path"] = "/".join(context.getPhysicalPath())

        new_keyword = to_str(new_keyword)
        try:
            querySet = api.content.find(**query)
        except UnicodeDecodeError:
            old_keywords = [
                k.decode("utf8") if isinstance(k, str) else k for k in old_keywords
            ]
            query[indexName] = old_keywords
            querySet = api.content.find(**query)
        for item in querySet:
            obj = item.getObject()
            # #MOD Dynamic field getting

            value = self.getFieldValue(obj, indexName)
            if isinstance(value, (list, tuple)):
                # MULTIVALUED FIELD
                value = list(value)
                for element in old_keywords:
                    while (element in value) and (element != new_keyword):
                        value[value.index(element)] = new_keyword

                # dedupe new Keyword list (an issue when combining multiple keywords)
                value = list(set(value))
            elif isinstance(value, set):
                value = value - set(old_keywords)
                value.add(new_keyword)
            else:
                # MONOVALUED FIELD
                value = new_keyword

                # #MOD Dynamic field update

            updateField = self.getSetter(obj, indexName)
            if updateField is not None:
                updateField(value)
                idxs = self._getFullIndexList(indexName)
                obj.reindexObject(idxs=idxs)

        return len(querySet)

    @security.protected(config.MANAGE_KEYWORDS_PERMISSION)
    def delete(self, keywords, context=None, indexName="Subject"):
        """Removes the keywords from all objects using it.

        Returns the number of objects that have been updated.
        """
        # #Mod Dynamic field
        query = {indexName: keywords}
        if context is not None:
            query["path"] = "/".join(context.getPhysicalPath())
        querySet = api.content.find(**query)

        for item in querySet:
            obj = item.getObject()
            value = self.getFieldValue(obj, indexName)
            if isinstance(value, (list, tuple)):
                # MULTIVALUED
                value = list(value)
                for element in keywords:
                    while element in value:
                        value.remove(element)
            elif type(value) is set:
                value = value - set(keywords)
            else:
                # MONOVALUED
                value = None

            updateField = self.getSetter(obj, indexName)
            if updateField is not None:
                updateField(value)
                idxs = self._getFullIndexList(indexName)
                obj.reindexObject(idxs=idxs)

        return len(querySet)

    @security.protected(config.MANAGE_KEYWORDS_PERMISSION)
    def getKeywords(self, context=None, indexName="Subject"):
        processQueue()
        if indexName not in self.getKeywordIndexes():
            raise ValueError("%s is not a valid field" % indexName)

        catalog = getToolByName(self, "portal_catalog")
        keywords = catalog.uniqueValuesFor(indexName)
        # Filter out empty keywords.  The sorting breaks when None is indexed.
        keywords = filter(None, keywords)
        return list(sorted(keywords, key=lambda x: x.lower()))

    @security.protected(config.MANAGE_KEYWORDS_PERMISSION)
    def getScoredMatches(self, word, possibilities, num, score, context=None):
        """ Take a word,
            compare it to a list of possibilities,
            return max. num matches > score).
        """
        if not USE_LEVENSHTEIN:
            # No levenshtein module around. Fall back to difflib
            return difflib.get_close_matches(word, possibilities, num, score)

        # Levenshtein is around, so let's use it.
        res = []

        # Search for all similar terms in possibilities
        if isinstance(word, str):
            oword = unicode(word, "utf-8")
        else:
            oword = word.encode("utf-8")

        for item in possibilities:
            if isinstance(item, type(word)):
                lscore = Levenshtein.ratio(word, item)
            elif isinstance(item, type(oword)):
                lscore = Levenshtein.ratio(oword, item)
            else:
                raise ValueError("%s is not a normal, or unicode string" % item)
            if lscore > score:
                res.append((item, lscore))

        # Sort by score (high scores on top of list)
        res.sort(lambda x, y: -cmp(x[1], y[1]))

        # Return first n terms without scores
        return [item[0] for item in res[:num]]

    def getKeywordIndexes(self):
        """Gets a list of indexes from the catalog. Uses config.py to choose the
        meta type and filters out a subset of known indexes that should not be
        managed.
        """
        catalog = getToolByName(self, "portal_catalog")
        idxs = catalog.index_objects()
        idxs = [
            i.id
            for i in idxs
            if i.meta_type == config.META_TYPE and i.id not in config.IGNORE_INDEXES
        ]
        idxs.sort()
        return idxs

    @security.private
    def fieldNameForIndex(self, indexName):
        """The name of the index may not be the same as the field on the object, and we need
           the actual field name in order to find its mutator.
        """
        catalog = getToolByName(self, "portal_catalog")
        indexObjs = [idx for idx in catalog.index_objects() if idx.getId() == indexName]
        try:
            fieldName = indexObjs[0].indexed_attrs[0]
        except IndexError:
            raise ValueError("Found no index named %s" % indexName)

        return fieldName

    @security.private
    def getSetter(self, obj, indexName):
        """Gets the setter function for the field based on the index name.

        Returns None if it can't get the function
        """

        # DefaultDublinCoreImpl:
        setterName = "set" + indexName
        if getattr(aq_base(obj), setterName, None) is not None:
            return getattr(obj, setterName)

        # other
        fieldName = self.fieldNameForIndex(indexName)
        field = None

        # Dexterity
        if IDexterityContent.providedBy(obj):
            if fieldName.startswith("get"):
                fieldName = fieldName.lstrip("get_")
            # heuristics
            fieldName = fieldName[0].lower() + fieldName[1:]
            return lambda value: setattr(aq_base(obj), fieldName, value)

        # AT and discussions left
        if IComment.providedBy(obj):
            # Discussion
            field = getattr(obj, "getField", None)
        else:
            # Archetype
            field = getattr(aq_base(obj), "getField", None)
        # Archetypes:
        if field:
            fieldObj = field(fieldName) or field(fieldName.lower())
            if not fieldObj and fieldName.startswith("get"):
                fieldName = fieldName.lstrip("get_")
                fieldName = fieldName[0].lower() + fieldName[1:]
                fieldObj = obj.getField(fieldName)
            if fieldObj is not None:
                return fieldObj.getMutator(obj)
            return None

        return None

    def getFieldValue(self, obj, indexName):
        fieldName = self.fieldNameForIndex(indexName)
        fieldVal = getattr(obj, fieldName, ())
        if not fieldVal and fieldName.startswith("get"):
            fieldName = fieldName.lstrip("get_")
            fieldName = fieldName[0].lower() + fieldName[1:]
            fieldVal = getattr(obj, fieldName, ())

        if callable(fieldVal):
            return fieldVal()
        else:
            return fieldVal


InitializeClass(PloneKeywordManager)
