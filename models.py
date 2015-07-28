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
    __tablename__ = 'fahrten'
    id = Column(Integer, primary_key=True)
    driver = Column(Text, nullable=False)
    abfahrtdatum = Column(Text, nullable=False)
    abfahrtzeit = Column(Text, nullable=False)
    ankunftdatum = Column(Text, nullable=False)
    ankunftzeit = Column(Text, nullable=False)
    startort = Column(Text, nullable=False)
    zielort = Column(Text, nullable=False)
    reisezweck = Column(Text, nullable=False)
    autokennzeichen = Column(Text, nullable=False)
    kilometerstand = Column(Text, nullable=False)
    
    def __init__(self, driver=None, abfahrtdatum=None, abfahrtzeit=None, ankunftdatum=None,ankunftzeit=None, startort=None, zielort=None,reisezweck=None, autokennzeichen=None, kilometerstand=None,):
        self.driver = driver
        self.abfahrtdatum = abfahrtdatum
        self.abfahrtzeit = abfahrtzeit
        self.ankunftdatum = ankunftdatum
        self.ankunftzeit = ankunftzeit
        self.startort = startort
        self.zielort = zielort
        self.reisezweck = reisezweck
        self.autokennzeichen = autokennzeichen
        self.kilometerstand = kilometerstand
                
    def __repr__(self):
        return '<%s(%r, %r, %r,%r, %r,%r, %r,%r, %r,%r )>' % (self.__class__.__name__, self.id, self.driver, self.abfahrtdatum, self.abfahrtzeit, self.ankunftdatum, self.ankunftzeit, self.startort, self.zielort, self.reisezweck, self.autokennzeichen, self.kilometerstand)
