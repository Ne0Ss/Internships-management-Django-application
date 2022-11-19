"""ProjetSI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Gestion import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('accueil/', views.accueil,name='accueil'),
    path('admin/', admin.site.urls),
    path('guide/', views.Guide,name='guide'),
    path('nous/', views.apropos,name='nous'),
    
    path('register/',views.register, name="register"),
    path('',views.loginPage,name="login" ),
    path('deconnecter/',views.deconnecterUtilisateur,name="logout" ),
    path('statistiques/<str:année>', views.stat,name='stat'),   

    path('etudiants/', views.etudiants,name='listeEtudiants'),
    path('etudiant/<str:matricule>',views.afficherEtudiant, name="detailEtudiant"),
    path('etudiant/creer/',views.creerEtudiant, name="creerEtudiant"),
    path('etudiant/modifier/<str:matricule>',views.modifierEtudiant, name="modifierEtudiant"),
    path('etudiant/supprimer/<str:matricule>',views.supprimerEtudiant, name="supprimerEtudiant"),
    path('ajouterequipe/',views.ajouterEquipe, name="ajouterEquipe"),
    path('etudiant/equipe/<str:NumEq>',views.modifierEquipe, name="modifierEquipe"),
    path('supprimer/equipe/<str:NumEq>',views.supprimerEquipe, name="supprimerEquipe"),
    path('etudiants/recherche/',views.rechercherEtudiants, name="rechercherEtudiant"),

    path('entreprises/', views.Entreprises,name='listeEntreprises'),
    path('entreprise/creer/',views.creerEntreprise, name="creerEntreprise"),
    path('entreprise/modifier/<str:Num>',views.modifierEntreprise, name="modifierEntreprise"),
    path('entreprise/supprimer/<str:Num>',views.supprimerEntreprise, name="supprimerEntreprise"),

    path('entreprise/<str:NumEnt>/promoteurs/', views.promoteurs,name='listePromoteurs'),
    path('entreprise/promoteur/<str:NumP>',views.afficherPromoteur, name="detailPromoteur"),
    path('entreprise/<str:NumEnt>/promoteur/creer/',views.creerPromoteur, name="creerPromoteur"),
    path('entreprise/promoteur/modifier/<str:NumP>',views.modifierPromoteur, name="modifierPromoteur"),
    path('entreprise/promoteur/supprimer/<str:NumP>',views.supprimerPromoteur, name="supprimerPromoteur"),

    path('entreprise/<str:NumEnt>/sujets/', views.sujets,name='listeSujets'),
    path('entreprise/sujet/<str:Num>',views.afficherSujet, name="detailSujet"),
    path('entreprise/<str:NumEnt>/sujet/creer/',views.creerSujet, name="creerSujet"),
    path('entreprise/sujet/modifier/<str:Num>',views.modifierSujet, name="modifierSujet"),
    path('entreprise/sujet/supprimer/<str:Num>',views.supprimerSujet, name="supprimerSujet"),

    path('encadrants/', views.encadrants,name='listeEncadrants'),
    path('encadrant/<str:Num>',views.afficherEncadrant, name="detailEncadrant"),
    path('encadrant/creer/',views.creerEncadrant, name="creerEncadrant"),
    path('encadrant/modifier/<str:Num>',views.modifierEncadrant, name="modifierEncadrant"),
    path('encadrant/supprimer/<str:Num>',views.supprimerEncadrant, name="supprimerEncadrant"),

    path('stages/', views.stages,name='listeStages'),
    path('stage/<str:Num>',views.afficherStage, name="detailStage"),
    path('stage/creer/',views.creerStage, name="creerStage"),
    path('stage/modifier/<str:Num>',views.modifierStage, name="modifierStage"),
    path('stage/supprimer/<str:Num>',views.supprimerStage, name="supprimerStage"),

    path('stage/sujet/<str:Num>',views.selectionnerSujet, name="selectionnerSujet"),
    path('stage/rapport/<str:Num>',views.entrerRapport, name="entrerRapport"),
    path('stage/<str:Num>/évaluation/',views.ajouterEvaluation, name="ajouterEvaluation"),
    path('stage/évaluation/modifier/<str:Num>',views.modifierEvaluation, name="modifierEvaluation"),
    
    path('stage/évaluation/Jury/',views.ajouterJury,name="ajouterJury"),
    path('stage/évaluation/Jury/supprimer/<str:Num>',views.supprimerJury,name="supprimerJury")
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)