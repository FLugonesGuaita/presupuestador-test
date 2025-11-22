from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class ClientData:
    nombre: str = ""
    documento: str = ""
    telefono: str = ""
    correo: str = ""
    direccion: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PlanData:
    plan_nombre: str = ""
    plan_cuota: str = ""
    plan_condiciones: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class VehicleData:
    modelo: str = ""
    anio: str = ""
    precio: str = ""
    color: str = ""
    version: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BudgetData:
    cliente: ClientData
    plan: PlanData
    vehiculo: VehicleData

    def to_flat_dict(self) -> Dict[str, str]:
        flat: Dict[str, str] = {}
        flat.update({f"cliente_{k}": str(v) for k, v in self.cliente.to_dict().items()})
        flat.update({f"plan_{k}": str(v) for k, v in self.plan.to_dict().items()})
        flat.update({f"vehiculo_{k}": str(v) for k, v in self.vehiculo.to_dict().items()})
        return flat
