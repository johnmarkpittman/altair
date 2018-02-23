import os

import pandas as pd
from IPython.display import display

from ...utils import PluginRegistry
from ..display import Displayable
from ..display import default_renderer as default_renderer_base
from ..display import json_renderer as json_renderer_base
from ..display import SpecType, MimeBundleType, RendererType



#==============================================================================
# Vega 3 renderer logic
#==============================================================================


# The MIME type for Vega 3 releases.
VEGA_MIME_TYPE = 'application/vnd.vega.v3+json'  # type: str

# The entry point group that can be used by other packages to declare other
# renderers that will be auto-detected. Explicit registration is also 
# allowed by the PluginRegistery API.
ENTRY_POINT_GROUP = 'altair.vega.v3.renderer'  # type: str

renderers = PluginRegistry[RendererType](entry_point_group=ENTRY_POINT_GROUP)


here = os.path.dirname(os.path.realpath(__file__))


def default_renderer(spec):
    return default_renderer_base(spec, VEGA_MIME_TYPE, '<Vega 3 object>')


def json_renderer(spec):
    return json_renderer_base(spec, '<Vega 3 object>')


renderers.register('default', default_renderer)
renderers.register('json', json_renderer)
renderers.enable('default')


class Vega(Displayable):
    """An IPython/Jupyter display class for rendering Vega 3."""

    renderers = renderers
    schema_path = os.path.join(here,'vega-schema.json')


def vega(spec: dict, validate=True):
    """Render and optionally validate a Vega 3 spec.

    This will use the currently enabled renderer to render the spec.

    Parameters
    ==========
    spec: dict
        A fully compliant VegaLite 1 spec, with the data portion fully processed.
    validate: bool
        Should the spec be validated against the Vega 3 schema?
    """
    display(Vega(spec, validate=validate))