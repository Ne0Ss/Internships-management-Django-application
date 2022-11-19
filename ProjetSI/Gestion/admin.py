from django.contrib import admin
from .models import Etudiant
from .models import Equipe
from .models import TypeStage
from .models import Stage
from .models import Entreprise
from .models import SujetPFE
from .models import Encadrant
from .models import Promoteur
from .models import FicheEvaluation
from .models import Jury

admin.site.register(Etudiant)
admin.site.register(Equipe)
admin.site.register(TypeStage)
admin.site.register(Stage)
admin.site.register(Entreprise)
admin.site.register(SujetPFE)
admin.site.register(Encadrant)
admin.site.register(Promoteur)
admin.site.register(FicheEvaluation)
admin.site.register(Jury) 
