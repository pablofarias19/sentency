import re
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ContextoAnalisis:
    palabra: str
    posicion: int
    contexto_completo: str
    es_negacion: bool
    es_condicional: bool
    es_ironico: bool
    es_positivo: bool
    confianza: float
    metadata: Dict

class ValidadorContextoRetorica:
    PATRONES_NEGACION = r"\b(no|nunca|jamás|falso|niega|erróneo|critic[ao])\b"
    PATRONES_CONDICIONAL = r"\b(si|aunque|suponiendo que|a menos que)\b"
    PATRONES_IRONIA = r"\b(aparentemente|supuestamente|al parecer)\b"
    PATRONES_DISTANCIA = r"\b(según algunos|hay quienes|ciertos autores|se dice que)\b"

    def __init__(self, ventana_contexto: int = 50):
        self.ventana_contexto = ventana_contexto

    def _ventana(self, texto, m):
        i = max(0, m.start()-self.ventana_contexto)
        f = min(len(texto), m.end()+self.ventana_contexto)
        return texto[i:f]

    def analizar_ethos(self, texto: str) -> List[ContextoAnalisis]:
        patrones = r"\b(CSJN|SCBA|tribunal|jurisprudencia|doctrina|autoridad|jurista|fallos|Fallos:|precedente)\b"
        res = []
        for m in re.finditer(patrones, texto, re.IGNORECASE):
            ctx = self._ventana(texto, m)
            neg  = bool(re.search(self.PATRONES_NEGACION, ctx, re.IGNORECASE))
            cond = bool(re.search(self.PATRONES_CONDICIONAL, ctx, re.IGNORECASE))
            iro  = bool(re.search(self.PATRONES_IRONIA, ctx, re.IGNORECASE))
            dist = bool(re.search(self.PATRONES_DISTANCIA, ctx, re.IGNORECASE))
            if neg or cond or iro or dist:
                pos, conf = False, 0.3
            else:
                pos, conf = True, 0.9
            res.append(ContextoAnalisis(
                palabra=m.group(),
                posicion=m.start(),
                contexto_completo=ctx,
                es_negacion=neg,
                es_condicional=cond,
                es_ironico=iro,
                es_positivo=pos,
                confianza=conf,
                metadata={"distancia": dist}
            ))
        return res

    def analizar_pathos(self, texto: str) -> List[ContextoAnalisis]:
        patrones = r"\b(crisis|urgencia|emergencia|riesgo|peligro|amenaza|culpa|indignación|escándalo|daño|grave|responsabilidad|injusticia)\b"
        res = []
        for m in re.finditer(patrones, texto, re.IGNORECASE):
            ctx = self._ventana(texto, m)
            neg  = bool(re.search(self.PATRONES_NEGACION, ctx, re.IGNORECASE))
            cond = bool(re.search(self.PATRONES_CONDICIONAL, ctx, re.IGNORECASE))
            pos, conf = (False, 0.3) if neg or cond else (True, 0.9)
            res.append(ContextoAnalisis(
                palabra=m.group(),
                posicion=m.start(),
                contexto_completo=ctx,
                es_negacion=neg,
                es_condicional=cond,
                es_ironico=False,
                es_positivo=pos,
                confianza=conf,
                metadata={}
            ))
        return res

    def analizar_logos(self, texto: str) -> List[ContextoAnalisis]:
        patrones = r"\b(porque|por lo tanto|ya que|en consecuencia|por consiguiente|luego|de ahí que)\b"
        res = []
        for m in re.finditer(patrones, texto, re.IGNORECASE):
            ctx = self._ventana(texto, m)
            pos, conf = True, 0.85
            res.append(ContextoAnalisis(
                palabra=m.group(),
                posicion=m.start(),
                contexto_completo=ctx,
                es_negacion=False,
                es_condicional=False,
                es_ironico=False,
                es_positivo=pos,
                confianza=conf,
                metadata={}
            ))
        return res