from pynwb import get_class, register_map
from .maze_extension import MazeExtension
from hdmf.build import ObjectMapper
from dateutil.parser import parse as dateutil_parse

LabMetaDataExtension = get_class('LabMetaDataExtension', 'ndx-tank-metadata')
RigExtension = get_class('RigExtension', 'ndx-tank-metadata')

# TODO: create issue at pynwb datetime issue (registering map, objectmapper)

#
# @register_map(LabMetaDataExtension)
# class LabMetaDataExtensionMap(ObjectMapper):
#
#     @ObjectMapper.constructor_arg('session_end_time')
#     def dateconversion(self, builder, manager):
#         datestr = builder.get('session_end_time').data
#         date = dateutil_parse(datestr)
#         return date
