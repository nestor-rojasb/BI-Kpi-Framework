# Casos de Uso por Industria

Este documento muestra cómo aplicar el framework de KPIs a diferentes industrias y contextos.

## E-commerce B2B

### Contexto
Plataforma de e-commerce que vende productos a empresas. Procesa miles de órdenes diarias con variabilidad en complejidad.

### Aplicación de KPIs

**1. Analyst Workload System**
- **Complejidad:** Número de SKUs por orden
- **Especialización:** Categoría de producto predominante
- **Uso:** Asignar órdenes a analistas según su especialización

**2. Operational Processing Monitor**
- **KPI 1 (Volumen):** Órdenes procesadas por analista
- **KPI 2 (Cumplimiento):** % de órdenes completadas vs asignadas
- **KPI 3 (Calidad):** % de órdenes sin errores de facturación

**3. Financial Performance**
- **Márgenes:** Por categoría de producto
- **Concentración:** Dependencia de proveedores específicos
- **Oportunidades:** Productos con bajo margen a optimizar

---

## Distribuidor Mayorista

### Contexto
Distribuidor que compra productos y los revende a retailers. Maneja múltiples categorías y cientos de proveedores.

### Aplicación de KPIs

**1. Analyst Workload System**
- **Complejidad:** Número de líneas en factura de proveedor
- **Especialización:** Tipo de producto (perecederos vs no perecederos)
- **Uso:** Balancear carga entre equipo de recepción

**2. Operational Processing Monitor**
- **KPI 1 (Volumen):** Facturas registradas
- **KPI 2 (Cumplimiento):** % de facturas procesadas a tiempo
- **KPI 3 (Calidad):** % sin discrepancias en montos

**3. Financial Performance**
- **Márgenes:** Por proveedor y categoría
- **Concentración:** Riesgo de dependencia de top proveedores
- **Oportunidades:** Negociación con proveedores de bajo margen

---

## Call Center

### Contexto
Centro de atención al cliente que maneja tickets de soporte técnico con diferentes niveles de complejidad.

### Aplicación de KPIs

**1. Analyst Workload System**
- **Complejidad:** Número de pasos/sistemas involucrados en la resolución
  - Muy Simple (1-2 pasos): Reseteo de password
  - Simple (3-5 pasos): Configuración básica
  - Moderado (6-10 pasos): Troubleshooting multi-sistema
  - Complejo (11+ pasos): Debugging avanzado
- **Especialización:** Tipo de producto/sistema
- **Uso:** Routing inteligente de tickets

**2. Operational Processing Monitor**
- **KPI 1 (Volumen):** Tickets cerrados
- **KPI 2 (Cumplimiento):** % de tickets resueltos en primera llamada
- **KPI 3 (Calidad):** % sin escalamiento

**3. Financial Performance**
- **Eficiencia:** Costo por ticket resuelto
- **Valor:** Tickets de alto valor vs recursos asignados

---

## Departamento de Cuentas por Pagar

### Contexto
Back-office corporativo que procesa facturas de múltiples departamentos y proveedores.

### Aplicación de KPIs

**1. Analyst Workload System**
- **Complejidad:** Número de cuentas contables por transacción
- **Especialización:** Tipo de gasto (capex vs opex, departamento)
- **Uso:** Asignación por especialidad contable

**2. Operational Processing Monitor**
- **KPI 1 (Volumen):** Facturas procesadas
- **KPI 2 (Cumplimiento):** % procesadas antes del vencimiento
- **KPI 3 (Calidad):** % sin errores de codificación contable

**3. Financial Performance**
- **Descuentos:** Aprovechamiento de descuentos por pronto pago
- **Concentración:** Dependencia de proveedores críticos
- **Oportunidades:** Consolidación de proveedores

---

## Operaciones de Procurement

### Contexto
Equipo de compras corporativas que gestiona RFQs, licitaciones y órdenes de compra.

### Aplicación de KPIs

**1. Analyst Workload System**
- **Complejidad:** Monto de la licitación + número de proveedores evaluados
- **Especialización:** Categoría de compra
- **Uso:** Asignación de licitaciones complejas a buyers senior

**2. Operational Processing Monitor**
- **KPI 1 (Volumen):** RFQs procesadas
- **KPI 2 (Cumplimiento):** % completadas en tiempo
- **KPI 3 (Calidad):** % sin requerimientos de re-cotización

**3. Financial Performance**
- **Ahorros:** Saving vs presupuesto original
- **Diversificación:** Balance en cartera de proveedores
- **Oportunidades:** Categorías con bajo nivel de competencia

---

## Centros de Servicios Compartidos (Shared Services)

### Contexto
SSC que procesa transacciones de múltiples unidades de negocio.

### Aplicación de KPIs

**1. Analyst Workload System**
- **Complejidad:** Número de entidades/países involucrados
- **Especialización:** Unidad de negocio o región
- **Uso:** Staffing por zona geográfica

**2. Operational Processing Monitor**
- **KPI 1 (Volumen):** Transacciones procesadas
- **KPI 2 (Cumplimiento):** % de SLA cumplidos
- **KPI 3 (Calidad):** % sin re-trabajos

**3. Financial Performance**
- **Costo por transacción:** Benchmark contra industria
- **Eficiencia:** Tendencia de costo vs volumen
- **Oportunidades:** Automatización de procesos de alto volumen

---

## Plataforma de Licitaciones Públicas

### Contexto
Proveedor del estado que participa en licitaciones y convenios marco.

### Aplicación de KPIs

**1. Analyst Workload System**
- **Complejidad:** Número de SKUs en la orden + monto
- **Especialización:** Tipo de producto (alimentos, aseo, tecnología)
- **Uso:** Especialización por rubro

**2. Operational Processing Monitor**
- **KPI 1 (Volumen):** Órdenes de compra procesadas
- **KPI 2 (Cumplimiento):** % entregadas en plazo
- **KPI 3 (Calidad):** % sin reclamos

**3. Financial Performance**
- **Márgenes:** Por tipo de licitación y cliente
- **Concentración:** Dependencia de organismos públicos específicos
- **Oportunidades:** Categorías con mejor margen

---

## Implementación General

### Pasos para Adaptar a Tu Contexto

1. **Identifica tu "unidad de trabajo"**
   - ¿Qué procesan tus analistas? (tickets, facturas, órdenes, casos)

2. **Define tu medida de complejidad**
   - ¿Qué hace que una tarea sea más difícil que otra?
   - Ejemplos: # de SKUs, # de pasos, # de sistemas, monto, # de aprobaciones

3. **Calibra tus pesos**
   - Haz un muestreo de tiempo real
   - Ajusta los pesos hasta que reflejen realidad

4. **Valida con tu equipo**
   - ¿Los analistas sienten que refleja su carga real?
   - ¿Los números "huelen bien"?

5. **Itera**
   - Los KPIs no son estáticos
   - Revisa y ajusta trimestralmente

---

## Preguntas Frecuentes

**P: ¿Necesito tener exactamente estos 3 KPIs?**
R: No. El principio es "pocos KPIs 100% confiables". Pueden ser 2, pueden ser 4, pero prioriza calidad sobre cantidad.

**P: ¿Los pesos de complejidad son universales?**
R: No. Los pesos deben calibrarse según tu realidad. Un ticket "complejo" en un call center no toma el mismo tiempo que una orden "compleja" en procurement.

**P: ¿Qué hago si mi organización ya tiene 20 KPIs?**
R: Audita cuáles son 100% confiables. Crea un "dashboard de bonos" con solo los confiables, y deja los demás como "informativos".

**P: ¿Funciona para equipos pequeños (2-3 personas)?**
R: Los KPIs de balance de carga son menos relevantes para equipos muy pequeños. Enfócate en las métricas financieras y de calidad.

**P: ¿Puedo usar esto para evaluar performance individual?**
R: Sí, pero con precaución. Los KPIs deben combinarse con evaluación cualitativa. Un analista con baja "carga ponderada" puede estar capacitando a otros, lo cual no se refleja en las métricas.
