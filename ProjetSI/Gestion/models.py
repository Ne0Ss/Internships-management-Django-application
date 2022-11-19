from django.db import models
import pkg_resources

Choix_année = (("1","1"),("2","2"),("3","3"),("4","4"),("5","5"))
class Etudiant(models.Model):
    Matricule = models.CharField(primary_key=True,max_length=8)
    NomE = models.CharField(max_length=40)
    PrénomE = models.CharField(max_length=50)
    NumeroE = models.CharField(max_length=10)
    EmailE = models.EmailField()
    DateNaiss = models.DateField()
    Spécialité = models.CharField(max_length=30)
    image = models.ImageField(upload_to='etudiants/images/',default="etudiants/images/noimg.png")
    Equipe = models.ForeignKey('Equipe',on_delete=models.CASCADE,null=False)
    def get_Matricule_Numbers(self):
        numbers=""
        for c in self.Matricule:
            if c.isdigit():
                numbers += c
        return numbers
    def __str__(self):
        return "{} {} ({})".format(self.NomE, self.PrénomE, self.Matricule)

class Equipe(models.Model):
    Stage = models.ForeignKey('Stage',on_delete=models.SET_NULL,null=True,blank=True)
    def listeEtudiants(self):
        etudiants= Etudiant.objects.all()
        l=[]
        for e in etudiants:
            if e.Equipe.pk==self.pk:
                l.append(e)
        return l
    def __str__(self):
        return "Equipe "+str(self.pk)

class TypeStage(models.Model):
    IntituléTS = models.CharField(max_length=50)
    Période = models.CharField(max_length=100)
    DuréeTS = models.CharField(max_length=50)
    NbEtudiants = models.CharField(max_length=50)
    def __str__(self):
        return self.IntituléTS
        
class Stage(models.Model):
    Durée = models.IntegerField() #en semaines
    DateDeb = models.DateField()
    Type = models.ForeignKey(TypeStage,on_delete=models.CASCADE,null=False)
    Encadrant = models.ForeignKey('Encadrant',on_delete=models.SET_NULL,null=True,blank=True)
    Promoteur = models.ForeignKey('Promoteur',on_delete=models.SET_NULL,null=True,blank=True)
    NumEnt = models.ForeignKey('Entreprise',on_delete=models.CASCADE,null=False)
    Fiche_Eval = models.ForeignKey('FicheEvaluation',on_delete=models.SET_NULL,null=True,blank=True)
    Sujet_pfe = models.ForeignKey('SujetPFE',on_delete=models.SET_NULL,null=True,blank=True)
    Rapport = models.FileField(upload_to='rapports/',null=True)
    def Equipe(self):
        try: 
            eq = Equipe.objects.get(Stage=self.pk)
            return eq
        except Equipe.DoesNotExist:
            return None
    def Year_stg(self):
        return self.DateDeb.year
    def __str__(self):
        return self.NumEnt.NomEnt+": "+self.Type.IntituléTS
    

class Entreprise(models.Model):
    NomEnt = models.CharField(max_length=50)
    RaisonSociale = models.CharField(max_length=50)
    Adresse = models.CharField(max_length=100)
    def listeSujets(self):
        sujets= SujetPFE.objects.all()
        l=[]
        for s in sujets:
            if s.NumEnt.pk==self.pk:
                l.append(s)
        return l
    def nbr_stagiaire(self):
        equipes= Equipe.objects.all()
        nbr=0
        for e in equipes:
            if e.Stage!=None:
                if e.Stage.NumEnt.pk == self.pk:
                    nbr += len(e.listeEtudiants())
        return nbr
    def __str__(self):
        return self.NomEnt

class SujetPFE(models.Model):
    IntituléS = models.CharField(max_length=50)
    Résumé = models.TextField()
    Plan = models.TextField()
    Date = models.DateTimeField()
    # Date = models.DateTimeField(auto_now=True)
    NumEnt = models.ForeignKey(Entreprise,on_delete=models.CASCADE,null=False)
    def __str__(self):
        return self.IntituléS

class Encadrant(models.Model):
    NomE = models.CharField(max_length=40)
    PrénomE = models.CharField(max_length=50)
    Domaine = models.CharField(max_length=50)
    NumeroE = models.CharField(max_length=10)
    EmailE = models.EmailField()
    image = models.ImageField(upload_to='encadrants/images/',default="encadrants/images/noimg.png")
    NumJury = models.ForeignKey('Jury',on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return "{} {} ({})".format(self.NomE, self.PrénomE, self.Domaine)

class Promoteur(models.Model):
    NomP = models.CharField(max_length=40)
    PrénomP = models.CharField(max_length=50)
    Profession = models.CharField(max_length=50)
    NumeroP = models.CharField(max_length=10)
    EmailP = models.EmailField()
    NumEnt = models.ForeignKey(Entreprise,on_delete=models.CASCADE,null=False)
    NumJury = models.ForeignKey('Jury',on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return "{} {} ({})".format(self.NomP, self.PrénomP, self.Profession)

class FicheEvaluation(models.Model):
    NoteRapport = models.FloatField()
    NoteRéalisation = models.FloatField()
    NoteSoutenance = models.FloatField()
    Jury = models.ForeignKey('Jury',on_delete=models.SET_NULL,null=True,blank=True)
    @property
    def NoteFinale(self):
        return (self.NoteRapport+2*self.NoteRéalisation+self.NoteSoutenance)/4
    def Stage(self):
        try: 
            s = Stage.objects.get(Fiche_Eval=self.pk)
            return s
        except Stage.DoesNotExist:
            return None

class Jury(models.Model):
    session = models.CharField(max_length=7,default='MM-AAAA')
    def __str__(self):
        return "session "+self.session
    def Encadrants(self):
        return Encadrant.objects.filter(NumJury=self.pk)
    def Promoteurs(self):
        return Promoteur.objects.filter(NumJury=self.pk)
