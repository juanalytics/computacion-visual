"""
Persistencia de eventos y métricas para el broker WebSocket.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

from sqlmodel import Field, Session, SQLModel, create_engine, select

# Streamlit y otros entornos interactivos pueden importar el módulo más de una vez;
# limpiamos la metainformación antes de volver a declarar las tablas para evitar
# errores del tipo "Table 'metricrecord' is already defined".
SQLModel.metadata.clear()


class MetricRecord(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: str
    module: str
    metric: str
    value: float


class CommandRecord(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: str
    module: str
    action: str
    source: str | None = None
    payload: str | None = None


@dataclass
class Storage:
    db_path: Path

    def __post_init__(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(f"sqlite:///{self.db_path}")
        SQLModel.metadata.create_all(self.engine)

    def add_metrics(self, module: str, timestamp: str, metrics: Dict[str, float]) -> None:
        if not metrics:
            return
        with Session(self.engine) as session:
            for key, value in metrics.items():
                session.add(
                    MetricRecord(
                        timestamp=timestamp,
                        module=module,
                        metric=key,
                        value=float(value),
                    )
                )
            session.commit()

    def add_command(self, module: str, timestamp: str, action: str, source: str | None, payload: str | None = None) -> None:
        with Session(self.engine) as session:
            session.add(
                CommandRecord(
                    timestamp=timestamp,
                    module=module,
                    action=action,
                    source=source,
                    payload=payload,
                )
            )
            session.commit()

    def latest_metrics(self, limit: int = 50) -> List[MetricRecord]:
        with Session(self.engine) as session:
            statement = select(MetricRecord).order_by(MetricRecord.id.desc()).limit(limit)
            return list(session.exec(statement))

    def recent_commands(self, limit: int = 20) -> List[CommandRecord]:
        with Session(self.engine) as session:
            statement = select(CommandRecord).order_by(CommandRecord.id.desc()).limit(limit)
            return list(session.exec(statement))

