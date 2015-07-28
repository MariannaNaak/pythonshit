from sqlalchemy import Column, Boolean, Integer, Text
from database import Base
from flask.ext.login import UserMixin
from hash_passwords import check_hash, make_hash

class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    def __init__(self, username=None, password=None, active=False):
        self.username = username
        self.password = password
        self.active = active

    def is_active(self):
        return self.active

    def get(id):
        if self.id == id:
            return self
        else:
            return None

    def valid_password(self, password):
        """Check if provided password is valid."""
        return check_hash(password, self.password)

    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.id, self.username)

class Fahrt(Base):
    __tablename__ = 'daten'
    
    id = Column(Integer, primary_key=True)
    Spielplatzname = Column(Text, nullable=False)
    Stadtteil = Column(Text, nullable=False)
    Stadtbezirk = Column(Text, nullable=False)
    Stadtviertel = Column(Text, nullable=False)
    Typ = Column(Text, nullable=False)
    Basketballkoerbe = Column(Text, nullable=False)
    Fussballtore = Column(Text, nullable=False)
    Skaterelemente = Column(Text, nullable=False)
    Tischtennisplatten = Column(Text, nullable=False)
    Torwand = Column(Text, nullable=False)
    Bemerkung = Column(Text, nullable=False)
    
    def __init__(self, Spielplatzname=None, Stadtteil=None, Stadtbezirk=None, Stadtviertel=None,Typ=None, Basketballkoerbe=None, Fussballtore=None,Skaterelemente=None, Tischtennisplatten=None, Torwand=None, Bemerkung=None):
        self.Spielplatzname = Spielplatzname
        self.Stadtteil = Stadtteil
        self.Stadtbezirk = Stadtbezirk
        self.Stadtviertel = Stadtviertel
        self.Typ = Typ
        self.Basketballkoerbe = Basketballkoerbe
        self.Fussballtore = Fussballtore
        self.Skaterelemente = Skaterelemente
        self.Tischtennisplatten = Tischtennisplatten
        self.Torwand = Torwand
        self.Bemerkung = Bemerkung
                
    def __repr__(self):
        return '<%s(%r, %r, %r,%r, %r,%r, %r,%r, %r,%r,%r )>' % (self.__class__.__name__, self.id, self.Spielplatzname, self.Stadtteil, self.Stadtbezirk, self.Stadtviertel, self.Typ, self.Basketballkoerbe, self.Fussballtore, self.Skaterelemente, self.Tischtennisplatten, self.Torwand, self.Bemerkung)
