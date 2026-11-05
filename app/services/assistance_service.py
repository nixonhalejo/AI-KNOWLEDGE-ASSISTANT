# app/services/assistance_service.py
import json
from app.provider.openrouter import OpenRouterProvider
from app.services.tools import tools_disponibles, consultar_base_interna

class AssistantService:
    def __init__(self, provider: OpenRouterProvider = None):
        self.provider = provider or OpenRouterProvider()

    async def ask(self, request) -> str:
        # 1. Historial inicial con la pregunta del usuario
        messages = [{"role": "user", "content": request.question}]
        
        # 2. Primer viaje: Enviamos la pregunta y las herramientas disponibles a la IA
        message_response = await self.provider.generate(
            messages=messages,
            temperature=request.temperature,
            top_p=request.top_p,
            max_tokens=request.max_tokens,
            tools=tools_disponibles
        )
        
        # 3. Verificamos si la IA decidió que necesita usar una herramienta ("tool_calls")
        if isinstance(message_response, dict) and "tool_calls" in message_response:
            tool_call = message_response["tool_calls"][0]
            function_name = tool_call["function"]["name"]
            function_args = json.loads(tool_call["function"]["arguments"])
            
            # Ejecutamos la función local de Python en tu servidor
            resultado_funcion = ""
            if function_name == "consultar_base_interna":
                resultado_funcion = consultar_base_interna(**function_args)
                
            # 4. Segundo viaje (Reenvío): Actualizamos el historial con la orden de la IA y el resultado obtenido
            messages.append(message_response) 
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": str(resultado_funcion)
            })
            
            # Llamamos nuevamente al proveedor para que la IA redacte la respuesta final con el dato real
            final_message = await self.provider.generate(
                messages=messages,
                temperature=request.temperature,
                top_p=request.top_p,
                max_tokens=request.max_tokens
            )
            return final_message if isinstance(final_message, str) else final_message.get("content", "")
        
        # Si la IA respondió directamente con texto (sin usar herramientas), devolvemos el contenido
        return message_response if isinstance(message_response, str) else message_response.get("content", "")