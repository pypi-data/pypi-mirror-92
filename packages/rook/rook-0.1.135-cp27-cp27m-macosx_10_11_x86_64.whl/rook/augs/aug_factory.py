"""This module is in charge of building a Aug object from it's over the wire form.

Since most serialization format do not support polymorphism, we add this capability in this module.

This module finds and loads all dynamic classes and dynamically builds the relevant component based on it's id.
"""

import re

import six

from rook.factory import Factory

from ..augs import actions, conditions, extractors, locations
from ..augs.aug import Aug


from rook.rookout_json import json
from rook import config

from rook.processor.processor_factory import ProcessorFactory

from rook.exceptions import ToolException, RookAugInvalidKey, RookObjectNameMissing, RookUnknownObject, RookInvalidObjectConfiguration, RookUnsupportedLocation


class AugFactory(Factory):
    """This is the factory for building Augs by their configuration."""

    def __init__(self, output):
        """Initialize the class."""
        super(AugFactory, self).__init__()

        self._output = output
        self._processor_factory = ProcessorFactory([], [])

        self._load_dynamic_classes()

    @staticmethod
    def get_dict_value(configuration, value, default_value):
        val = configuration.get(value)
        return val if val is not None else default_value

    def get_aug(self, configuration):
        """Returns an Aug object based on the given configuration."""
        try:
            aug_id = configuration['id']
        except KeyError as exc:
            six.raise_from(RookAugInvalidKey('id', json.dumps(configuration)), exc)

        try:
            locationDict = configuration['location']
        except KeyError as exc:
            six.raise_from(RookAugInvalidKey('location', json.dumps(configuration)), exc)
        location = self._get_dynamic_class(locationDict)

        if 'extractor' in configuration:
            extractor = self._get_dynamic_class(configuration['extractor'])
        else:
            extractor = None

        condition = None
        conditional = configuration.get('conditional')
        if conditional:
            condition = conditions.IfCondition(conditional)

        try:
            actionDict = configuration['action']
        except KeyError as exc:
            six.raise_from(RookAugInvalidKey('action', json.dumps(configuration)), exc)
        action = self._get_dynamic_class(actionDict)

        limits_spec = configuration.get('rateLimit', None)
        rate_limits = None

        if limits_spec:
            r = re.match(r'^(\d+)/(\d+)$', limits_spec)

            if r is not None:
                rate_limits = (int(r.group(1)), int(r.group(2)))

        if not rate_limits:
            rate_limits = (200, 5000)

        max_aug_execution_time = AugFactory.get_dict_value(configuration, 'maxAugTime', config.InstrumentationConfig.MAX_AUG_TIME)

        return Aug(aug_id=aug_id,
                   location=location,
                   extractor=extractor,
                   condition=condition,
                   action=action,
                   output=self._output,
                   max_aug_execution_time=max_aug_execution_time,
                   rate_limits=rate_limits)

    def _load_dynamic_classes(self):
        """Load all dynamic classes into the factory."""
        self.register_methods(locations.__all__)
        self.register_methods(extractors.__all__)
        self.register_methods(conditions.__all__)
        self.register_methods(actions.__all__)

    def _get_dynamic_class(self, configuration):
        """Return a class based on configuration."""

        if not configuration:
            return None
        else:
            try:
                name = configuration['name']
            except KeyError as exc:
                six.raise_from(RookObjectNameMissing(json.dumps(configuration)), exc)

            try:
                factory = self.get_object_factory(name)
            except (RookUnknownObject, AttributeError, KeyError) as exc:
                six.raise_from(RookUnsupportedLocation(name), exc)

            try:
                return factory(configuration, self._processor_factory)
            except ToolException:
                raise
            except Exception as exc:
                six.raise_from(RookInvalidObjectConfiguration(name, json.dumps(configuration)), exc)
