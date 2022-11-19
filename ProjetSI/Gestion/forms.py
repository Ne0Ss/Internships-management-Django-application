from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class FicheEtudiant(ModelForm):
    class Meta:
        model = Etudiant
        fields = '__all__'

class FicheEquipe(ModelForm):
    class Meta:
        model = Equipe
        fields = '__all__'

class FicheEntreprise(ModelForm):
    class Meta:
        model = Entreprise
        fields = '__all__'


class FichePromoteur(ModelForm):
    class Meta:
        model = Promoteur
        fields = '__all__'
        # exclude = ('NumEnt',)

class FicheSujet(ModelForm):
    class Meta:
        model = SujetPFE
        fields = '__all__'

class FicheEncadrant(ModelForm):
    class Meta:
        model = Encadrant
        fields = '__all__'

class FicheStage(ModelForm):
    class Meta:
        model = Stage 
        exclude = ('Fiche_Eval','Sujet_pfe','Rapport',)

class FicheModifierStage(ModelForm):
    class Meta:
        model = Stage
        exclude = ('Fiche_Eval',)

class FicheEntrerRapport(ModelForm):
    class Meta:
        model = Stage
        fields = ["Rapport"] 

class FormFicheEvaluation(ModelForm): 
    class Meta:
        model = FicheEvaluation
        fields = '__all__'
        
class FicheJury(ModelForm): 
    class Meta:
        model = Jury
        fields = '__all__'