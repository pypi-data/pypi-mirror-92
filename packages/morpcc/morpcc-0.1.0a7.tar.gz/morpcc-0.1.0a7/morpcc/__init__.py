from . import patches
import logging

from .app import App
from .crud.model import CollectionUI, ModelUI
from .root import Root
from .static import StaticRoot
from .wizard.wizard import AgreementWizardStep, FormWizardStep, Wizard, WizardStep

log = logging.getLogger("morpcc")
