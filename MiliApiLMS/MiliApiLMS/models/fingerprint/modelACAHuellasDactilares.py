from MiliApiLMS import sqlServer

class ACAHuellaDactilar(sqlServer.Model):
    #tabla ACAHuellasDactilares
    __tablename__ = 'ACAHuellasDactilaresFingerPrint'
    #__tablename__ = 'ACAHuellasDactilares'
    #__table_args__ = {'extend_existing': True} # allows you to modify the existing table without raising an error.
    CodigoHuellaDactilar = sqlServer.Column(sqlServer.Integer, primary_key=True)
    CodigoDedo = sqlServer.Column(sqlServer.Integer, nullable=False)
    CodigoPersona = sqlServer.Column(sqlServer.Integer, nullable=False)
    FechaRegistro = sqlServer.Column(sqlServer.DateTime, nullable=False)
    Huella = sqlServer.Column(sqlServer.VARBINARY, nullable=False)
    CodigoUsuario = sqlServer.Column(sqlServer.String(50), nullable=False)
    HuellaEsValida = sqlServer.Column(sqlServer.Boolean, nullable=False)
    
    def __init__(self, CodigoDedo, CodigoPersona, FechaRegistro, Huella, CodigoUsuario, HuellaEsValida):
        self.CodigoDedo = CodigoDedo
        self.CodigoPersona = CodigoPersona
        self.FechaRegistro = FechaRegistro
        self.Huella= Huella
        self.CodigoUsuario = CodigoUsuario
        self.HuellaEsValida = HuellaEsValida
        
    #def __repr__(self):
    #    return f'Huella: CodigoDedo={self.CodigoDedo}, CodigoPersona={self.CodigoPersona}, FechaRegistro={self.FechaRegistro}, Huella={self.Huella}, CodigoUsuario={self.CodigoUsuario}, HuellaEsValida={self.HuellaEsValida}'

    #def __str__(self):
    #    return self.CodigoHuellaDactilar
