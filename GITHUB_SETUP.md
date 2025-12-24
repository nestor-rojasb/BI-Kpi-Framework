# Guía para Subir el Proyecto a GitHub

## Paso 1: Crear el Repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `bi-kpi-framework`
3. Descripción: `Business Intelligence KPI Framework - Modular system for B2B operations analytics`
4. Público/Privado: Tu elección
5. **NO** inicialices con README, .gitignore o License (ya los tenemos)
6. Click en "Create repository"

## Paso 2: Preparar el Repositorio Local

Abre tu terminal y navega al directorio del proyecto:

```bash
cd bi-kpi-framework
```

## Paso 3: Inicializar Git

```bash
# Inicializar repositorio
git init

# Agregar todos los archivos
git add .

# Hacer el primer commit
git commit -m "Initial commit: Business Intelligence KPI Framework

- Sistema de carga laboral de analistas (workload)
- Sistema 3-KPI de procesamiento operacional
- Métricas de performance financiera
- Generador de datos sintéticos
- Documentación completa de metodología
- Notebooks de ejemplo"

```

## Paso 4: Conectar con GitHub

Reemplaza `TU-USUARIO` con tu nombre de usuario de GitHub:

```bash
# Agregar remote
git remote add origin https://github.com/TU-USUARIO/bi-kpi-framework.git

# Renombrar rama a main (si es necesario)
git branch -M main

# Subir a GitHub
git push -u origin main
```

## Paso 5: Verificar

Ve a `https://github.com/TU-USUARIO/bi-kpi-framework` y verifica que:
- ✓ README.md se muestra correctamente
- ✓ Todos los archivos están presentes
- ✓ La estructura de carpetas es correcta

## Paso 6: Configurar GitHub Pages (Opcional)

Si quieres tener una página web del proyecto:

1. Ve a Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: / (root)
4. Save

## Estructura Final del Repositorio

```
bi-kpi-framework/
│
├── README.md                    ← Se muestra en la página principal
├── LICENSE                      ← MIT License
├── .gitignore                   ← Archivos a ignorar
├── requirements.txt             ← Dependencias Python
├── demo.py                      ← Script de demostración rápida
│
├── data/
│   ├── schema/                  ← (vacío - para tu implementación)
│   └── synthetic/               ← Datos de ejemplo generados
│       ├── generate_data.py     ← Generador de datos
│       ├── suppliers.csv
│       ├── skus.csv
│       ├── analysts.csv
│       ├── purchase_orders.csv
│       ├── order_lines.csv
│       └── invoices.csv
│
├── src/
│   ├── kpis/
│   │   ├── analyst_workload.py      ← Sistema de carga laboral
│   │   ├── invoice_processing.py    ← Sistema 3-KPI
│   │   └── financial_metrics.py     ← KPIs financieros
│   ├── core/                        ← (para expansión futura)
│   └── viz/                         ← (para dashboards)
│
├── notebooks/
│   └── 01_analyst_workload.ipynb    ← Análisis interactivo
│
├── docs/
│   ├── methodology.md               ← Metodología detallada
│   └── use_cases.md                 ← Casos de uso por industria
│
└── examples/                        ← (para casos específicos)
```

## Mejoras Sugeridas para el Perfil

### Agregar Topics (Tags) al Repositorio

En la página de GitHub, click en el ⚙️ al lado de "About" y agrega:

- `business-intelligence`
- `kpi`
- `data-analysis`
- `python`
- `analytics`
- `operations`
- `b2b`
- `performance-metrics`

### Descripción del Repositorio

```
Modular KPI framework for B2B operations analytics. Includes analyst workload system, operational processing monitor, and financial metrics - all based on production-tested methodologies.
```

### Website (si tienes)

Puedes agregar un link a tu portfolio o LinkedIn.

## Comandos Git Útiles para el Futuro

```bash
# Ver estado de cambios
git status

# Agregar cambios específicos
git add archivo.py

# Agregar todos los cambios
git add .

# Hacer commit
git commit -m "Descripción del cambio"

# Subir cambios
git push

# Ver historial
git log --oneline

# Crear nueva rama para feature
git checkout -b feature/nueva-funcionalidad

# Volver a main
git checkout main

# Merge de rama
git merge feature/nueva-funcionalidad
```

## Promoción del Proyecto

### En tu CV/LinkedIn:

```
Business Intelligence KPI Framework
- Desarrollé un framework modular de KPIs para operaciones B2B
- Implementé 3 sistemas principales: carga laboral, procesamiento operacional, y métricas financieras
- Metodología probada en producción con miles de transacciones diarias
- Framework generalizable a múltiples industrias (e-commerce, distribución, procurement)
- GitHub: github.com/TU-USUARIO/bi-kpi-framework
```

### README Badge Sugeridos:

Agrega al inicio del README.md:

```markdown
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
```

## Troubleshooting

**Error: "remote origin already exists"**
```bash
git remote remove origin
git remote add origin https://github.com/TU-USUARIO/bi-kpi-framework.git
```

**Error al hacer push (authentication)**
- Usa Personal Access Token en vez de password
- Genera en: GitHub → Settings → Developer settings → Personal access tokens

**Archivos grandes (.csv)**
- Los .gitignore ya excluye archivos procesados
- Los CSVs sintéticos son pequeños (~2MB) y están incluidos

## Próximos Pasos Sugeridos

1. **Agregar tests unitarios**
   - `pytest` para validar cálculos de KPIs

2. **Crear dashboard interactivo**
   - Streamlit o Plotly Dash

3. **Documentar API**
   - Docstrings completas
   - Generar con Sphinx

4. **Agregar más ejemplos**
   - Notebooks por industria
   - Casos de uso específicos

5. **Crear GitHub Actions**
   - CI/CD para tests automáticos

---

¡Listo! Tu proyecto ya está preparado para GitHub y para impresionar en entrevistas. 🚀
