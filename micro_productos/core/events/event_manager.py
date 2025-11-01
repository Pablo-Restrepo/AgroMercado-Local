import asyncio
from typing import Callable, Dict, List, Any


class EventManager:
    """
    Implementa el patrón Observer.
    Permite registrar callbacks (suscriptores) para eventos específicos
    y notificarlos de manera asíncrona.
    """
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable[..., Any]):
        """Registra un callback para un evento."""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)

    async def notify(self, event_name: str, data: Any):
        """Notifica de manera asíncrona a todos los suscriptores."""
        callbacks = self._subscribers.get(event_name, [])
        tasks = [asyncio.create_task(callback(data)) for callback in callbacks]
        if tasks:
            await asyncio.gather(*tasks)
