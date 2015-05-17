import logging
import os
import errno
from Products.CMFCore.utils import getToolByName
from collective.documentviewer.config import EXTENSION_TO_ID_MAPPING
from collective.documentviewer.config import CONVERTABLE_TYPES
from collective.documentviewer.interfaces import IFileWrapper


def getDocumentType(obj, allowed_types):
    ct = IFileWrapper(obj).file_type
    if ct is None:
        logging.debug('getDocumentType: No File type for %s' % obj.id)
        return None

    logging.debug('getDocumentType: File type %s for %s' % (
        ct, obj.id))
    mime_registry = getToolByName(obj, 'mimetypes_registry')
    for _type in mime_registry.lookup(ct):
        logging.debug('getDocumentType: lookup type %s for %s' % (
         _type, obj.id))
        for ext in _type.extensions:
            logging.debug('getDocumentType: lookup ext %s for %s' % (
                ext, obj.id))
            if ext in EXTENSION_TO_ID_MAPPING:
                id = EXTENSION_TO_ID_MAPPING[ext]
                if id in allowed_types:
                    logging.debug('getDocumentType: id %s FOUND for %s' % (
                        id, obj.id))
                    return CONVERTABLE_TYPES[id]
                else:
                    logging.debug('getDocumentType: id %s NOT FOUND for %s' % (
                        id, obj.id))
            else:
                logging.debug('getDocumentType: ext %s inot FOUND for %s' % (
                    ext, obj.id))

    logging.debug('getDocumentType: not FOUND for %s' % (obj.id))
    return None


def allowedDocumentType(object, allowed_types):
    return getDocumentType(object, allowed_types) is not None


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise


def getPortal(obj):
    return getToolByName(obj, 'portal_url').getPortalObject()
