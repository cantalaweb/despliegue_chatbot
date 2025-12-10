# 🐳 Guía Docker y DockerHub

## Pre-requisitos
- Docker Desktop instalado y corriendo
- Cuenta en DockerHub (https://hub.docker.com)

## 1. Construir la Imagen Localmente

```bash
# Desde el directorio raíz del proyecto
docker build -t llm-chat-agent .
```

## 2. Probar Localmente

```bash
# Asegúrate de tener el archivo .env con tu OPENAI_API_KEY
docker run -d \
  --name chat-agent \
  -p 8000:8000 \
  --env-file .env \
  llm-chat-agent

# Verificar que está corriendo
docker ps

# Ver logs
docker logs chat-agent

# Acceder a la aplicación
open http://localhost:8000/chat
```

## 3. Limpiar Contenedores de Prueba

```bash
# Detener el contenedor
docker stop chat-agent

# Eliminar el contenedor
docker rm chat-agent

# (Opcional) Eliminar la imagen
docker rmi llm-chat-agent
```

## 4. Subir a DockerHub

### Paso 1: Login en DockerHub
```bash
docker login
# Introduce tu usuario y contraseña de DockerHub
```

### Paso 2: Etiquetar la Imagen
```bash
# Reemplaza <tu-usuario> con tu usuario de DockerHub
docker tag llm-chat-agent <tu-usuario>/llm-chat-agent:latest
docker tag llm-chat-agent <tu-usuario>/llm-chat-agent:v1.0
```

### Paso 3: Subir la Imagen
```bash
# Subir versión latest
docker push <tu-usuario>/llm-chat-agent:latest

# Subir versión específica
docker push <tu-usuario>/llm-chat-agent:v1.0
```

## 5. Descargar y Usar desde DockerHub

Cualquier persona puede ahora descargar y ejecutar tu imagen:

```bash
# Descargar la imagen
docker pull <tu-usuario>/llm-chat-agent:latest

# Ejecutar con su propia API key
docker run -d \
  --name chat-agent \
  -p 8000:8000 \
  -e OPENAI_API_KEY=sk-tu-api-key-aqui \
  <tu-usuario>/llm-chat-agent:latest
```

## 6. Comandos Útiles

### Ver imágenes locales
```bash
docker images
```

### Ver contenedores en ejecución
```bash
docker ps
```

### Ver todos los contenedores (incluso detenidos)
```bash
docker ps -a
```

### Entrar al contenedor en ejecución
```bash
docker exec -it chat-agent sh
```

### Ver logs en tiempo real
```bash
docker logs -f chat-agent
```

### Detener y eliminar todo
```bash
docker stop chat-agent
docker rm chat-agent
docker rmi llm-chat-agent
```

## 7. Variables de Entorno

### Con archivo .env
```bash
docker run -d --name chat-agent -p 8000:8000 --env-file .env llm-chat-agent
```

### Con variable directa
```bash
docker run -d --name chat-agent -p 8000:8000 \
  -e OPENAI_API_KEY=sk-tu-key \
  llm-chat-agent
```

## 8. Persistencia de Datos

Si quieres que la base de datos persista entre reinicios del contenedor:

```bash
docker run -d \
  --name chat-agent \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  llm-chat-agent
```

## 9. Verificar Health Check

```bash
# Desde dentro del contenedor
docker exec chat-agent curl http://localhost:8000/health

# Desde tu máquina
curl http://localhost:8000/health
```

## 10. Troubleshooting

### Contenedor no arranca
```bash
# Ver logs detallados
docker logs chat-agent

# Verificar que el puerto 8000 no está en uso
lsof -i :8000
```

### Falta API key
```bash
# Verificar variables de entorno dentro del contenedor
docker exec chat-agent env | grep OPENAI
```

### Rebuild forzado
```bash
# Rebuild sin caché
docker build --no-cache -t llm-chat-agent .
```

## 11. Para la Presentación

### Setup rápido antes de la demo:
```bash
# 1. Construir imagen
docker build -t llm-chat-agent .

# 2. Ejecutar
docker run -d --name chat-agent -p 8000:8000 --env-file .env llm-chat-agent

# 3. Verificar
curl http://localhost:8000/health

# 4. Abrir en navegador
open http://localhost:8000/chat
```

### Durante la demo:
```bash
# Mostrar que está corriendo en Docker
docker ps

# Mostrar logs si hay tiempo
docker logs chat-agent --tail 20

# Mostrar información de la imagen
docker images llm-chat-agent
```

---

## 📝 Checklist para DockerHub

- [ ] Cuenta creada en DockerHub
- [ ] Login exitoso: `docker login`
- [ ] Imagen construida: `docker build -t llm-chat-agent .`
- [ ] Imagen probada localmente
- [ ] Imagen etiquetada: `docker tag llm-chat-agent <usuario>/llm-chat-agent:latest`
- [ ] Imagen subida: `docker push <usuario>/llm-chat-agent:latest`
- [ ] Verificar en https://hub.docker.com que aparece
- [ ] Probar descargar en otra terminal: `docker pull <usuario>/llm-chat-agent:latest`

---

**¡Imagen lista para la presentación!** 🚀
