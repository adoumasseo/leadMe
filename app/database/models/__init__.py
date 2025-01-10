from .university import Universite
from .ecole import Ecole
from .filiere import Filiere
from .matiere import Matiere
from .post import Post
from .serie import Serie
from .user import User
from .associations import Moyenne
from .associations import MatiereFiliere
from .associations import Coefficient
from .associations import Note

__all__ = [
    "Universite", "Ecole", "Filiere", "Matiere", "Post", "Serie", 
    "User", "Moyenne", "MatiereFiliere", "Coefficient", "Note"
]