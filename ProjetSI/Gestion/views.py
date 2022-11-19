from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required


# @login_required(login_url='login')
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,"Un compte a été créé pour "+user)
            return redirect("accueil")
        elif request.POST.get('password1')!=request.POST.get('password2'):
            messages.info(request,'Les mots de passe ne sont pas identiques.')
        else:
            messages.info(request,'Veuillez entrer un mot de passe valide:\nMinimum 8 caracteres alphanumériques.')
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form":form})

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect("accueil")
        else:
            messages.info(request,"Username ou mot de passe incorrecte.")
    context = {}
    return render(request, "registration/login.html",context)

def deconnecterUtilisateur(request):
    logout(request)
    return redirect('login')

# @login_required(login_url='login')
def accueil(request):
    return render(request,'accueil.html')

def stat(request):
    return render(request,'stat.html')

def EquipesVides():
    EV=[]
    ENV=[]
    for etudiant in Etudiant.objects.all():
        ENV.append(etudiant.Equipe.pk)
    for equipe in Equipe.objects.all():
        if equipe.pk not in ENV:
            EV.append(equipe.pk)
    return EV

def etudiants(request):
    etudiants = Etudiant.objects.all()
    equipes = Equipe.objects.all()
    # stage = Stage.objects.all()
    # rapport = Rapport.objects.all()
    # ficheEvaluation = FicheEvaluation.objects.all()
    # jury = Jury.objects.all()
    context = {"equipes":equipes,"etudiants":etudiants,"equipesNonVide":EquipesVides()}
    return render(request,'etudiants/etudiants.html',context)

# @login_required(login_url='login')
def rechercherEtudiants(request):
    etudiants = []
    if request.method =="GET":
        query=request.GET.get('recherche')
        Etudiants = Etudiant.objects.all()
        if query!=None:
            for e in Etudiants:
                if query in str(e):
                    etudiants.append(e)
    context = {"etudiants":etudiants}
    return render(request,"etudiants/rechercheEtudiants.html",context)

def afficherEtudiant(request,matricule):
    matricule = matricule[0:2]+'/'+matricule[2:7]
    e = Etudiant.objects.get(Matricule=matricule)
    return render(request, 'etudiants/detail.html', context={'etudiant': e})

def nombre_participation(matricule):
    i=0
    for etudiant in Etudiant.objects.all():
        if etudiant.Matricule[0:7] == matricule[0:7]:
            i+=1
    return i

def matricule_valide(matricule):
    return str(matricule)[2]=="/" and len(matricule)==8

def creerEtudiant(request):
    form = FicheEtudiant()
    if request.method == 'POST':
        form = FicheEtudiant(request.POST,request.FILES)
        equipe = Equipe.objects.get(pk=request.POST.get('Equipe'))
        if form.is_valid() and matricule_valide(request.POST.get('Matricule')) and nombre_participation(request.POST.get('Matricule'))<3 and len(equipe.listeEtudiants())<4:
            form.save()
            return redirect('/etudiants')
        if str(request.POST.get('Matricule'))[2]!="/" or len(request.POST.get('Matricule'))<8:
            messages.info(request,"Matricule non valide.")
        if nombre_participation(request.POST.get('Matricule'))>=3:
            messages.info(request,"Nombre de stages maximum atteint pour cet étudiant.")
        if len(equipe.listeEtudiants())==4:
            messages.info(request,"Nombre maximal d'étudiants dans l'"+str(equipe)+" atteint.")
    # for champ in form:
    #     print(champ.name)
    context = {'form':form}
    return render(request, 'etudiants/ficheEtudiant.html',context)

def modifierEtudiant(request,matricule):
    matricule = matricule[0:2]+'/'+matricule[2:7]
    e = Etudiant.objects.get(Matricule=matricule)
    form = FicheEtudiant(instance=e)
    if request.method == 'POST':
        form = FicheEtudiant(request.POST,request.FILES,instance=e)
        if form.is_valid():
            form.save()
            return redirect('/etudiants')
    context = {'form':form}
    return render(request, 'etudiants/ficheEtudiant.html',context)

def supprimerEtudiant(request,matricule):
    matricule = matricule[0:2]+'/'+matricule[2:7]
    e = Etudiant.objects.get(Matricule=matricule)
    if request.method == 'POST':
        e.delete()
        return redirect('/etudiants')
    context = {'etudiant':e}
    return render(request,'etudiants/supprimer.html',context)

def ajouterEquipe(request):
    form = FicheEquipe()
    if request.method == "POST":
        form = FicheEquipe(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/etudiant/creer/')
    context = {"form":form}
    return render(request, "etudiants/ficheEquipe.html",context)

def Check_NbrEtudiant_Equipe(eq,stage):
    nbrEtu=len(eq.listeEtudiants())
    typeStage=stage.Type.pk
    if typeStage==1 and nbrEtu in [1,2]:
        return True,"valide"
    elif typeStage==2 and nbrEtu in [1,2,3,4]:
        return True,"valide"
    elif typeStage==3 and nbrEtu==2:
        return True,"valide"
    elif typeStage==1:
        return False,"Le stage ouvrier ne peut etre effectué qu'en monôme ou en binôme, or, il y a "+str(nbrEtu)+" dans l'"+str(eq)+"."
    elif typeStage==3:
        return False,"Le stage PFE ne peut etre effectué qu'en binôme, or, il y a "+str(nbrEtu)+" dans l'"+str(eq)+"."

def modifierEquipe(request,NumEq):
    eq = Equipe.objects.get(pk=NumEq)
    form = FicheEquipe(instance=eq)
    if request.method == 'POST':
        stage = Stage.objects.get(pk=request.POST.get('Stage'))
        form = FicheEquipe(request.POST,instance=eq)
        check,msg = Check_NbrEtudiant_Equipe(eq,stage)
        if form.is_valid() and check and stage.Equipe()==None:
            form.save()            
            return redirect('listeEtudiants')
        elif not check:
            messages.info(request,msg)
        elif stage.Equipe()!=None:
            messages.info(request,"L'"+str(stage.Equipe())+" est déjà assignée à ce stage.")
    context = {'form':form,'equipe':eq}
    return render(request, 'etudiants/modifierEquipe.html',context)


def supprimerEquipe(request,NumEq):
    eq = Equipe.objects.get(pk=NumEq)
    if request.method == 'POST':
        eq.delete()
        return redirect('/etudiants')
    context = {'equipe':eq}
    return render(request,'etudiants/supprimerEquipe.html',context)

def Entreprises(request):
    entreprises = Entreprise.objects.all()
    return render(request, "entreprises/Entreprises.html",{'entreprises':entreprises})

def creerEntreprise(request):
    form = FicheEntreprise()
    if request.method == 'POST':
        form = FicheEntreprise(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/entreprises')
    context = {'form':form}
    return render(request, 'entreprises/ficheEntreprise.html',context)

def modifierEntreprise(request,Num):
    e = Entreprise.objects.get(pk=Num)
    form = FicheEntreprise(instance=e)
    if request.method == 'POST':
        form = FicheEntreprise(request.POST,instance=e)
        if form.is_valid():
            form.save()
            return redirect('/entreprises')
    context = {'form':form}
    return render(request, 'entreprises/ficheEntreprise.html',context)

def supprimerEntreprise(request,Num):
    ent = Entreprise.objects.get(pk=Num)
    if request.method == 'POST':
        ent.delete()
        return redirect('/entreprises')
    context = {'entreprise':ent}
    return render(request,'entreprises/supprimerEntreprise.html',context)

def promoteurs(request,NumEnt):
    promoteurs = Promoteur.objects.filter(NumEnt = NumEnt)
    entreprise = Entreprise.objects.get(pk = NumEnt)
    context ={"promoteurs":promoteurs,"entreprise":entreprise}
    return render(request,'promoteurs/promoteurs.html',context)

def afficherPromoteur(request,NumP):
    p = Promoteur.objects.get(pk=NumP)
    return render(request, 'promoteurs/detail.html', context={'promoteur': p})

def creerPromoteur(request,NumEnt):
    entreprise = Entreprise.objects.get(pk = NumEnt)
    form = FichePromoteur()
    if request.method == 'POST':
        updated_request = request.POST.copy()
        updated_request.update({
        'NumEnt': NumEnt})
        form = FichePromoteur(updated_request)
        if form.is_valid():
            form.save()
            return redirect('/entreprises')
    context = {'form':form,'entreprise':entreprise}
    return render(request, 'promoteurs/fichePromoteur.html',context)

def modifierPromoteur(request,NumP):
    p = Promoteur.objects.get(pk=NumP)
    entreprise = Entreprise.objects.get(pk = p.NumEnt.pk)
    form = FichePromoteur(instance=p)
    if request.method == 'POST':
        updated_request = request.POST.copy()
        updated_request.update({
        'NumEnt': p.NumEnt})
        form = FichePromoteur(updated_request,instance=p)
        if form.is_valid():
            form.save()
            return redirect('/entreprises')
    context = {'form':form,'promoteur':p,'entreprise':entreprise}
    return render(request, 'promoteurs/fichePromoteur.html',context)

def supprimerPromoteur(request,NumP):
    p = Promoteur.objects.get(pk=NumP)
    if request.method == 'POST':
        p.delete()
        return redirect('/entreprises')
    context = {'promoteur':p}
    return render(request,'promoteurs/supprimerPromoteur.html',context)

def sujets(request,NumEnt):
    sujets = SujetPFE.objects.filter(NumEnt = NumEnt)
    entreprise = Entreprise.objects.get(pk = NumEnt)
    context ={"sujets":sujets,"entreprise":entreprise}
    return render(request,'sujets/sujets.html',context)

def afficherSujet(request,Num):
    s = SujetPFE.objects.get(pk=Num)
    return render(request, 'sujets/detail.html', context={'sujet': s})

def creerSujet(request,NumEnt):
    entreprise = Entreprise.objects.get(pk = NumEnt)
    form = FicheSujet()
    if request.method == 'POST':
        updated_request = request.POST.copy()
        updated_request.update({
        'NumEnt': NumEnt})
        form = FicheSujet(updated_request)
        if form.is_valid():
            form.save()
            return redirect('/entreprises')
    context = {'form':form,'entreprise':entreprise}
    return render(request, 'sujets/ficheSujet.html',context)

def modifierSujet(request,Num):
    s = SujetPFE.objects.get(pk=Num)
    entreprise = Entreprise.objects.get(pk = s.NumEnt.pk)
    form = FicheSujet(instance=s)
    if request.method == 'POST':
        updated_request = request.POST.copy()
        updated_request.update({
        'NumEnt': s.NumEnt})
        form = FicheSujet(updated_request,instance=s)
        if form.is_valid():
            form.save()
            return redirect('/entreprises')
    context = {'form':form,'sujet':s,'entreprise':entreprise}
    return render(request, 'sujets/ficheSujet.html',context)

def supprimerSujet(request,Num):
    s = SujetPFE.objects.get(pk=Num)
    if request.method == 'POST':
        s.delete()
        return redirect('/entreprises')
    context = {'sujet':s}
    return render(request,'sujets/supprimerSujet.html',context)

def encadrants(request):
    encadrants = Encadrant.objects.all()
    return render(request,'encadrants/encadrants.html',context={'encadrants':encadrants})

def creerEncadrant(request):
    form = FicheEncadrant()
    if request.method == 'POST':
        form = FicheEncadrant(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/encadrants')
    context = {'form':form}
    return render(request, 'encadrants/ficheEncadrant.html',context)

def modifierEncadrant(request,Num):
    e = Encadrant.objects.get(pk=Num)
    form = FicheEncadrant(instance=e)
    if request.method == 'POST':
        form = FicheEncadrant(request.POST,request.FILES,instance=e)
        if form.is_valid():
            form.save()
            return redirect('/encadrants')
    context = {'form':form,'encadrant':e}
    return render(request, 'encadrants/ficheEncadrant.html',context)

def supprimerEncadrant(request,Num):
    enc = Encadrant.objects.get(pk=Num)
    if request.method == 'POST':
        enc.delete()
        return redirect('/encadrants')
    context = {'encadrant':enc}
    return render(request,'encadrants/supprimerEncadrant.html',context)

def afficherEncadrant(request,Num):
    e = Encadrant.objects.get(pk=Num)
    return render(request, 'encadrants/detail.html', context={'encadrant': e})

def Guide(request):
    return render(request,'guide.html')

def stages(request):
    stages = Stage.objects.all()
    return render(request,'stages/stages.html',context={'stages':stages})

def check_durée_stage(durée,typeStage):
    if typeStage==1 and int(durée)==2:
        return True,"valide"
    elif typeStage==2 and int(durée) in [6,7,8]:
        return True,"valide"
    elif typeStage==3 and int(durée)<=40 and int(durée)>=24:
        return True,"valide"
    elif typeStage==1:
        return False,"La durée d'un stage ouvrier doit etre de 2 semaines."
    elif typeStage==2:
        return False,"La durée d'un stage technique doit etre compris entre 6 à 8 semaines."
    elif typeStage==3:
        return False,"La durée d'un stage PFE doit etre compris entre 24 à 40 semaines."

def creerStage(request):
    form = FicheStage()
    if request.method == 'POST':
        form = FicheStage(request.POST,request.FILES)
        if form.is_valid():
            type = TypeStage.objects.get(pk=request.POST.get('Type'))
            check,msg = check_durée_stage(request.POST.get('Durée'),type.pk)
            if check:
                if request.POST.get('Encadrant')!="" and type.pk==1:
                    messages.info(request,"Le stage ouvrier ne fait pas objet d'un double encadrement.")
                else:
                    form.save()
                    return redirect('listeStages')
            else:
                messages.info(request,msg)
        messages.info(request,form.errors)
    context = {'form':form}
    return render(request, 'stages/ficheStage.html',context)


from PyPDF2 import PdfFileReader

def check_nbr_pages(nbr,typeStage):
    if typeStage==1 and nbr>6:
        return "Attention: Le rapport comporte "+str(nbr)+" pages il dépasse les 6 pages maximales!"
    elif typeStage==2 and nbr>20:
        return "Attention: Le rapport comporte "+str(nbr)+" pages il dépasse les 20 pages maximales!"
    elif typeStage==3 and nbr>120:
        return "Attention: Le rapport comporte "+str(nbr)+" pages il dépasse les 120 pages maximales!"
    else:
        return ""

def modifierStage(request,Num):
    s = Stage.objects.get(pk=Num)
    form = FicheModifierStage(instance=s)
    if s.Rapport!="":
        pdf = PdfFileReader(open('static/'+str(s.Rapport),'rb'))
        checkRapport = check_nbr_pages(pdf.getNumPages(),s.Type.pk)
    else:
        checkRapport=""
    if request.method == 'POST':
        form = FicheModifierStage(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            return redirect('listeStages')
    context = {'form':form,'stage':s,'msgRapport':checkRapport}
    return render(request, 'stages/modifierStage.html',context)

def supprimerStage(request,Num):
    s = Stage.objects.get(pk=Num)
    if request.method == 'POST':
        s.delete()
        return redirect('listeStages')
    context = {'stage':s}
    return render(request,'stages/supprimerStage.html',context)

def afficherStage(request,Num):
    s = Stage.objects.get(pk=Num)
    e = s.Equipe()
    if e!=None:
        liste=e.listeEtudiants()
    else: liste=[]
    context={'stage': s,'etudiants': liste}
    return render(request, 'stages/detail.html',context)


def selectionnerSujet(request,Num):
    s = Stage.objects.get(pk=Num)
    entreprise = Entreprise.objects.get(pk = s.NumEnt.pk)
    sujets=entreprise.listeSujets()
    if request.method == 'POST':
        Stage.objects.filter(pk=Num).update(Sujet_pfe=request.POST.get('sujet'))
        return redirect('listeStages')
    context={'sujets':sujets,'entreprise':entreprise,'stage':s}
    return render(request,'stages/selectionnerSujet.html',context)

def entrerRapport(request,Num):
    s = Stage.objects.get(pk=Num)
    form = FicheEntrerRapport(instance=s)
    if request.method == 'POST':
        form = FicheEntrerRapport(request.POST,request.FILES,instance=s)
        if form.is_valid():
            form.save()
            return redirect('listeStages')
    context = {'form':form,'stage':s}
    return render(request, 'stages/entrerRapport.html',context)

def ajouterEvaluation(request,Num):
    s = Stage.objects.get(pk=Num)
    form = FormFicheEvaluation()
    if request.method == 'POST':
        form = FormFicheEvaluation(request.POST)
        if form.is_valid():
            e = form.save()
            Stage.objects.filter(pk=Num).update(Fiche_Eval=e.pk)
            return redirect('listeStages')
    context = {'form':form,'stage':s}
    return render(request,'stages/ajouterEvaluation.html',context)

def modifierEvaluation(request,Num):
    f = FicheEvaluation.objects.get(pk=Num)
    s = f.Stage()
    form = FormFicheEvaluation(instance=f)
    if request.method == 'POST':
        form = FormFicheEvaluation(request.POST,instance=f)
        if form.is_valid():
            form.save()
            return redirect('listeStages')
    context = {'form':form,'stage':s}
    return render(request,'stages/ajouterEvaluation.html',context)

def ajouterJury(request):
    form = FicheJury()
    if request.method == "POST":
        form = FicheJury(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listeStages')
    context = {"form":form}
    return render(request, "Jury/ficheJury.html",context)

def supprimerJury(request,Num):
    j = Jury.objects.get(pk=Num)
    if request.method == 'POST':
        j.delete()
        return redirect('listeStages')
    context = {'jury':j}
    return render(request,'Jury/supprimerJury.html',context)

def Pfe_Org(année):
    entreprises = Entreprise.objects.all()
    NomEnts=[]
    NbrS=[]
    for e in entreprises:
        i=0
        sujets = SujetPFE.objects.filter(NumEnt = e.pk)
        for s in sujets:
            if s.Date.year == int(année):
                i+=1
        NbrS.append(i)
        NomEnts.append(e.NomEnt)
    return NomEnts,NbrS

def stat(request,année):
    liste1,liste2 = Pfe_Org(année)
    liste3,liste4= tauxEvolution()
    liste5,liste6= Nbr_Stg_Ent()
    now = datetime.datetime.now()
    AnnéeCourante = now.year
    context = {
        'NomOrg':liste1,
        'NbrPfe':liste2,
        'année':année,
        'listeAnnées':list(map(str,list(range(2015,int(AnnéeCourante)+1)))),
        'NbrEnt':liste3,
        'an':liste4,
        'NomEnt':liste5,
        'NbrStg':liste6,
    }
    return render(request,'statistiques/stat.html',context)

def equipePfeAnnée(année):
    equipes = Equipe.objects.all()
    l=[]
    for e in equipes:
        if e.Stage!=None:
            if e.Stage.Year_stg() == année and e.Stage.Type.pk == 3:
                l.append(e) 
    return l

def tauxEvolution():
    now = datetime.datetime.now()
    années = list(range(2015,now.year))
    NbrEnt = []
    for année in années:
        equipes = equipePfeAnnée(année)
        entreprises=[]
        for equipe in equipes:
            if equipe.Stage.NumEnt not in entreprises:
                entreprises.append(equipe.Stage.NumEnt)
        NbrEnt.append(len(entreprises))
    return NbrEnt ,années 
        
def Nbr_Stg_Ent():
    entreprises = Entreprise.objects.all()
    NomEnts=[]
    NbrStg=[]
    for e in entreprises:
        NbrStg.append(e.nbr_stagiaire())
        NomEnts.append(e.NomEnt)
    return NomEnts,NbrStg

def apropos(request):
    return render(request,"àpropos.html")