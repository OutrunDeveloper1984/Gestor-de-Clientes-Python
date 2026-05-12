# Gestor de clientes con Python

Este proyecto consiste en una aplicación del tipo CRUD (Create, Read, Update, Delete) para el registro de clientes, mediante una interfaz gráfica, y un menú en terminal, donde el usuario puede acceder a las diferentes funciones de la aplicación

## Características principales
- CRUD de clientes
- Persistencia de datos mediante SQLite
- Interfaz gráfica
- Modo consola
- Pruebas unitarias

## Evolución del proyecto

Originalmente el proyecto utilizaba archivos CSV como sistema de base de datos.
Posteriormente fue refactorizado para utilizar SQLite, tomando como referencia la arquitectura de un proyecto previo basado en CSV

## Cambios realizados durante la migración 
- Reemplazo de lectura/escritura CSV por consultas SQLite
- Separación de la lógica de acceso a datos con un módulo dedicado
- Adaptación de pruebas unitarias
- Corrección de errores relacionados con persistencia
- Manejo consistente de conexiones a la base de datos
- Mejora en validaciones y manejo de errores

## Motivo del cambio
La migración a SQLite permitió:
  - Mejor consistencia de datos
  - Escalabilidad
  - Consultlas mas eficientes
  - Código mas mantenible
  - Simulación mas realista de una base de datos
