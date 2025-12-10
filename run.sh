#!/bin/bash

# Script para ejecutar la aplicación LLM Chat Agent
# Uso: ./run.sh [local|docker]

set -e

echo "🤖 LLM Chat Agent - Launcher"
echo "=============================="
echo ""

# Verificar que existe .env
if [ ! -f .env ]; then
    echo "⚠️  Archivo .env no encontrado"
    echo "Creando .env desde .env.example..."
    cp .env.example .env
    echo "✅ Archivo .env creado"
    echo "⚠️  IMPORTANTE: Edita el archivo .env y añade tu OPENAI_API_KEY"
    echo ""
    read -p "¿Has configurado tu API key en .env? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Por favor, edita .env y ejecuta este script de nuevo"
        exit 1
    fi
fi

MODE=${1:-local}

if [ "$MODE" == "docker" ]; then
    echo "🐳 Modo: Docker"
    echo ""

    # Verificar que Docker está corriendo
    if ! docker info > /dev/null 2>&1; then
        echo "❌ Docker no está corriendo"
        echo "Por favor, inicia Docker Desktop e intenta de nuevo"
        exit 1
    fi

    # Construir imagen
    echo "📦 Construyendo imagen Docker..."
    docker build -t llm-chat-agent .

    # Detener contenedor previo si existe
    if docker ps -a | grep -q chat-agent; then
        echo "🧹 Limpiando contenedor anterior..."
        docker stop chat-agent 2>/dev/null || true
        docker rm chat-agent 2>/dev/null || true
    fi

    # Ejecutar contenedor
    echo "🚀 Iniciando contenedor..."
    docker run -d \
        --name chat-agent \
        -p 8000:8000 \
        --env-file .env \
        llm-chat-agent

    # Esperar a que el servidor arranque
    echo "⏳ Esperando a que el servidor esté listo..."
    for i in {1..10}; do
        if curl -s http://localhost:8000/health > /dev/null; then
            break
        fi
        sleep 1
    done

    echo ""
    echo "✅ Aplicación corriendo en Docker"
    echo ""
    echo "📊 Comandos útiles:"
    echo "  - Ver logs:    docker logs -f chat-agent"
    echo "  - Detener:     docker stop chat-agent"
    echo "  - Eliminar:    docker rm chat-agent"

elif [ "$MODE" == "local" ]; then
    echo "💻 Modo: Local"
    echo ""

    # Verificar que existe el entorno virtual
    if [ ! -d .venv ]; then
        echo "📦 Instalando dependencias..."
        uv sync
    fi

    echo "🚀 Iniciando servidor..."
    echo ""
    cd src
    ../.venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000

else
    echo "❌ Modo no válido: $MODE"
    echo "Uso: ./run.sh [local|docker]"
    exit 1
fi

echo ""
echo "🌐 Accede a la aplicación:"
echo "  - Frontend:  http://localhost:8000/chat"
echo "  - API Docs:  http://localhost:8000/docs"
echo "  - Landing:   http://localhost:8000/"
echo ""
