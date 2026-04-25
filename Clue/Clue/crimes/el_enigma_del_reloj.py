"""
el_enigma_del_reloj.py — El Enigma del Reloj de Arena(Bono)

El legendario Reloj de Arena de Isfahan fue reemplazado por una réplica de cristal durante la gala del museo.
El ladrón tuvo que acceder a la vitrina principal y evadir los sensores de peso.
La Jefa de Seguridad Beatrice tiene coartada verificada por las cámaras del circuito exterior.
El Conservador Arthur posee acceso a la vitrina principal y tiene deudas secretas de juego.
La Coleccionista Clara tiene deudas con un traficante de arte, pero no posee acceso a la vitrina.
El Pasante Damian no posee acceso a la vitrina ni tiene deudas conocidas.
Fibras de seda azul del abrigo del Conservador Arthur aparecen enganchadas en la réplica de cristal.
La réplica de cristal es el objeto del crimen.
El Conservador Arthur, la Coleccionista Clara y el Pasante Damian no tienen coartada verificada.
El Conservador Arthur acusa a la Coleccionista Clara.
La Coleccionista Clara acusa al Conservador Arthur.
El Pasante Damian declara que el Conservador Arthur estuvo organizando los archivos con él a la hora del robo.

Como detective, he llegado a las siguientes conclusiones:
Quien tiene coartada verificada por medios objetivos queda descartado.
Quien posee acceso a la vitrina y tiene deudas tiene el medio y el motivo para el robo.
Quien deja fibras de su ropa en el objeto del crimen tiene evidencia física en su contra.
Quien tiene medio y motivo, sin coartada y con evidencia física en su contra es culpable.
Cuando el culpable acusa a otra persona para desviar la investigación, esa acusación es un desvío sospechoso.
Quien da falsa coartada al culpable está encubriendo el crimen.
Una acusación es corroborada cuando el acusador carece de acceso a la vitrina pero el acusado tiene evidencia física.
"""

from src.crime_case import CrimeCase, QuerySpec
from src.predicate_logic import ExistsGoal, ForallGoal, KnowledgeBase, Predicate, Rule, Term

def crear_kb() -> KnowledgeBase:
    kb = KnowledgeBase()
    
    #constantes del caso
    jefa_beatrice       = Term("jefa_beatrice")
    conservador_arthur  = Term("conservador_arthur")
    coleccionista_clara = Term("coleccionista_clara")
    pasante_damian      = Term("pasante_damian")
    replica_cristal     = Term("replica_cristal")
    vitrina_principal   = Term("vitrina_principal")
    seda_azul           = Term("seda_azul")
    
    X = Term("$X")
    Y = Term("$Y")
    
    #hechos
    kb.add_fact(Predicate("grabado_por_camara", (jefa_beatrice,)))
    kb.add_fact(Predicate("acceso_vitrina_principal", (conservador_arthur, vitrina_principal)))
    kb.add_fact(Predicate("tiene_deudas", (conservador_arthur,)))
    kb.add_fact(Predicate("tiene_deudas", (coleccionista_clara,)))
    kb.add_fact(Predicate("fibras_de_seda_azul", (conservador_arthur, replica_cristal, seda_azul)))
    kb.add_fact(Predicate("acusa", (conservador_arthur, coleccionista_clara)))
    kb.add_fact(Predicate("acusa", (coleccionista_clara, conservador_arthur)))
    kb.add_fact(Predicate("da_coartada", (pasante_damian, conservador_arthur)))
    
    #reglas
    #Quien tiene coartada verificada por medios objetivos queda descartado.
    kb.add_rule(Rule(
        head = Predicate("descartado", (X,)),
        body = (Predicate("grabado_por_camara", (X,)),)
    ))
    
    #Quien posee acceso a la vitrina y tiene deudas tiene el medio y el motivo para el robo.
    kb.add_rule(Rule(
        head = Predicate("tiene_medio_y_motivo", (X,)),
        body = (Predicate("acceso_vitrina_principal", (X, vitrina_principal)),
               Predicate("tiene_deudas", (X,)),)
    ))
    
    #Quien deja fibras de su ropa en el objeto del crimen tiene evidencia física en su contra.
    kb.add_rule(Rule(
        head = Predicate("tiene_evidencia_fisica_en_contra", (X,)),
        body = (Predicate("fibras_de_seda_azul", (X, replica_cristal, seda_azul)),)
    ))
    
    #Quien tiene medio y motivo, sin coartada y con evidencia física en su contra es culpable.
    kb.add_rule(Rule(
        head = Predicate("culpable", (X,)),
        body = (Predicate("tiene_medio_y_motivo", (X,)),
                Predicate("tiene_evidencia_fisica_en_contra", (X,)),)
    ))
    
    #Cuando el culpable acusa a otra persona para desviar la investigación, esa acusación es un desvío sospechoso.
    kb.add_rule(Rule(
        head = Predicate("desvio_sospechoso", (X,)),
        body = (Predicate("culpable", (X,)),
                Predicate("acusa", (X, Y)),)
    ))
    
    #Quien da falsa coartada al culpable está encubriendo el crimen.
    kb.add_rule(Rule(
        head = Predicate("encubriendo_al_culpable", (X,)),
        body = (Predicate("da_coartada", (X, Y)), 
                Predicate("culpable", (Y,)))
    ))
    
    #Una acusación es corroborada cuando el acusador carece de acceso a la vitrina pero el acusado tiene evidencia física.
    kb.add_rule(Rule(
        head = Predicate("acusacion_valida", (X, Y)),
        body = (Predicate("acusa", (X, Y)),
                Predicate("tiene_evidencia_fisica_en_contra", (Y,)),)
    ))
    
    return kb

CASE = CrimeCase(
    id = "el_enigma_del_reloj",
    title = "El Enigma del Reloj de Arena",
    suspects = ("jefa_beatrice", "conservador_arthur", "coleccionista_clara", "pasante_damian"),
    narrative =__doc__,
    description = (
        "El legendario Reloj de Arena fue cambiado por una réplica. "
        "Arthur tiene acceso y deudas, además de fibras de seda en la escena. "
        "Beatrice fue grabada por cámaras. Damian le da coartada a Arthur. "
        "Arthur y Clara se acusan mutuamente."
    ),
    create_kb = crear_kb,
    queries =( 
        QuerySpec(
            description="¿Está la Jefa Beatrice descartada por las cámaras?",
            goal=Predicate("descartado", (Term("jefa_beatrice"),)),
        ),
        
        QuerySpec(
            description="¿Es el Conservador Arthur el culpable del robo?",
            goal=Predicate("culpable", (Term("conservador_arthur"),)),
        ),
        
        QuerySpec(
            description="¿Está el Pasante Damian encubriendo al culpable?",
            goal=Predicate("encubriendo_al_culpable", (Term("pasante_damian"),)),
        ),
        
        QuerySpec(
            description="¿Existe algún sospechoso que haya realizado un desvío sospechoso?",
            goal=ExistsGoal("$X", Predicate("desvio_sospechoso", (Term("$X"),))),
        ),
        
        QuerySpec(
            description="¿Se cumple que todos los grabados por cámara están descartados?",
            goal=ForallGoal(
                "$X", 
                Predicate("grabado_por_camara", (Term("$X"),)),
                Predicate("descartado", (Term("$X"),))        
            ),
        ),
    ),
)