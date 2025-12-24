# Metodología de KPIs

## Filosofía General

Este framework se basa en tres principios fundamentales:

1. **Confiabilidad sobre Cantidad**: Es mejor tener 3 KPIs 100% confiables que 10 KPIs donde dudas de la calidad de los datos.

2. **Contexto sobre Volumen**: Una métrica de "cantidad" sin considerar complejidad es engañosa. Un ticket con 100 SKUs no es igual a un ticket con 1 SKU.

3. **Accionable sobre Informativo**: Cada KPI debe impulsar una decisión específica, no solo "informar".

---

## 1. Analyst Workload System

### Problema que Resuelve

Los sistemas tradicionales miden carga de trabajo solo por volumen de tickets/transacciones. Esto ignora completamente la complejidad:
- Un analista con 100 tickets simples (1 SKU cada uno)
- Un analista con 50 tickets complejos (50+ SKUs cada uno)

En sistemas de conteo simple, el segundo analista aparece como "menos productivo" cuando en realidad está procesando más trabajo.

### Solución: Ponderación por Complejidad

**Categorías de Complejidad:**

| Categoría | Rango SKUs | Peso | Tiempo Estimado |
|-----------|------------|------|-----------------|
| Muy Simple | 1-5 | 1.0x | Base |
| Simple | 6-20 | 2.5x | 2.5x base |
| Moderado | 21-50 | 5.0x | 5x base |
| Complejo | 51+ | 10.0x | 10x base |

**Fórmula de Carga Ponderada:**

```
Carga Total = Σ (Número de Tickets × Peso de Complejidad)
```

### Métricas Derivadas

1. **Carga Ponderada Total**: Suma de todos los tickets × sus pesos
2. **Promedio SKUs por Ticket**: Indica el tipo de trabajo que maneja cada analista
3. **Distribución por Complejidad**: Muestra especialización natural
4. **Ratio de Desbalance**: Max carga / Min carga entre analistas

### Aplicaciones Prácticas

#### Call Centers
- Tickets simples: Reseteo de password
- Tickets complejos: Configuración de sistema multiusuario
- **Peso**: Número de pasos/sistemas involucrados

#### Soporte Técnico
- Tickets simples: Problemas de conexión
- Tickets complejos: Debugging de aplicación
- **Peso**: Número de logs/sistemas a revisar

#### Análisis Financiero
- Transacciones simples: Pago único
- Transacciones complejas: Conciliación multibanco
- **Peso**: Número de cuentas/registros involucrados

### Interpretación de Resultados

**Coeficiente de Variación (CV) de Carga:**
- **CV < 20%**: Distribución balanceada
- **20% ≤ CV < 30%**: Desbalance leve - monitorear
- **CV ≥ 30%**: Desbalance significativo - redistribuir

**Especialización:**
- **> 60% en una categoría**: Especialista nato
- **30-60% distribuido**: Generalista
- **< 30% concentración**: Necesita enfoque

---

## 2. Operational Processing Monitor (3-KPI System)

### Problema que Resuelve

Muchas organizaciones tienen dashboards con 10, 15, 20 KPIs. El problema:
- ¿Cuáles son 100% confiables?
- ¿Cuáles están basados en estimaciones?
- ¿Cuáles tienen lags en actualización?

Cuando tienes dudas sobre los datos, **ningún KPI es útil**.

### Solución: Solo 3 KPIs, 100% Confiables

#### KPI 1: VOLUMEN
**Qué mide:** Cantidad procesada (registros, facturas, órdenes, etc.)

**Fuente de datos:** Conteo directo en tabla transaccional

**Confiabilidad:** 100% - Es un `COUNT(*)` directo

**Acción que impulsa:** Asignación de recursos

```sql
SELECT assigned_to, COUNT(*) as volume
FROM transactions
WHERE week = X
GROUP BY assigned_to
```

#### KPI 2: CUMPLIMIENTO
**Qué mide:** % de lo asignado que se completó

**Fuente de datos:** Registro de asignaciones vs. completados

**Confiabilidad:** 100% - Basado en flags binarios (asignado/completado)

**Acción que impulsa:** Identificación de cuellos de botella

```sql
SELECT assigned_to, 
       COUNT(*) as assigned,
       SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed,
       (completed / assigned * 100) as completion_pct
FROM tasks
WHERE week = X
GROUP BY assigned_to
```

#### KPI 3: CALIDAD
**Qué mide:** % procesado sin errores

**Fuente de datos:** Flag de error en registro transaccional

**Confiabilidad:** 100% - Campo binario (error/no error)

**Acción que impulsa:** Detección de necesidad de entrenamiento

```sql
SELECT assigned_to,
       COUNT(*) as total,
       SUM(CASE WHEN has_error = 0 THEN 1 ELSE 0 END) as no_errors,
       (no_errors / total * 100) as quality_pct
FROM transactions
WHERE week = X
GROUP BY assigned_to
```

### Por Qué Solo 3 KPIs

**KPIs Excluidos Intencionalmente:**

| Métrica | Por Qué NO se Incluye |
|---------|----------------------|
| Tiempo promedio de procesamiento | Requiere timestamps precisos (pueden tener lags) |
| Satisfacción del cliente | Basado en encuestas (sample, no población) |
| Tasa de retrabajos | Requiere tracking adicional (posible subestimación) |
| Eficiencia vs. benchmark | Requiere datos externos (puede cambiar) |

**Principio:** Si no puedes garantizar 100% de confiabilidad, NO lo incluyas en el dashboard semanal de bonos.

### Frecuencia de Reporte

- **Semanal**: Para decisiones de bonos/performance
- **Mensual**: Para análisis de tendencias
- **Trimestral**: Para evaluaciones formales

### Umbrales Sugeridos

Estos varían por industria, pero un punto de partida:

| KPI | Verde (Excelente) | Amarillo (Aceptable) | Rojo (Requiere Acción) |
|-----|------------------|---------------------|----------------------|
| Volumen | > Promedio + 10% | Promedio ± 10% | < Promedio - 10% |
| Cumplimiento | ≥ 98% | 95-97% | < 95% |
| Calidad | ≥ 98% | 95-97% | < 95% |

---

## 3. Financial Performance Metrics

### Problema que Resuelve

Las operaciones B2B generan volumen, pero ¿generan valor?
- ¿Qué proveedores son más rentables?
- ¿Qué categorías tienen mejores márgenes?
- ¿Tenemos riesgo de concentración?

### Métricas Clave

#### Margen por Transacción
```
Margen % = (Precio Venta - Costo) / Costo × 100
```

**Interpretación:**
- < 10%: Margen bajo - revisar pricing o costos
- 10-20%: Margen saludable B2B
- \> 20%: Margen alto - posible ventaja competitiva

#### Concentración de Proveedores (Índice HHI)

**Herfindahl-Hirschman Index:**
```
HHI = Σ (market_share_i)²
```

Donde `market_share_i` = (Compras al proveedor i / Total compras) × 100

**Interpretación:**
- **HHI < 1,500**: Baja concentración (bajo riesgo)
- **1,500 ≤ HHI < 2,500**: Concentración moderada
- **HHI ≥ 2,500**: Alta concentración (alto riesgo)

**Ejemplo:**
Si tus Top 3 proveedores representan 70% de tus compras, tienes alto riesgo de dependencia.

#### Análisis por Categoría

Identifica qué categorías de producto generan más valor:

```python
Valor = Volumen × Margen %
```

**Matriz de Decisión:**

| | Alto Margen | Bajo Margen |
|------------|-------------|-------------|
| **Alto Volumen** | ⭐ Priorizar | ⚠️ Optimizar precio |
| **Bajo Volumen** | 💎 Nicho rentable | ❌ Considerar descontinuar |

---

## Implementación en Tu Organización

### 1. Identifica Tus Fuentes de Datos

**Pregunta clave:** ¿Qué datos tengo 100% confiables?

No adaptes tus datos a estos KPIs - adapta estos KPIs a tus datos confiables.

### 2. Empieza Simple

- Semana 1-2: Implementa solo el sistema 3-KPI
- Semana 3-4: Agrega análisis de carga laboral
- Mes 2+: Incorpora métricas financieras

### 3. Valida con Tu Equipo

Antes de usar KPIs para bonos/evaluaciones:
1. Corre 4 semanas de prueba
2. Pide feedback a los analistas
3. Ajusta pesos/umbrales según necesidad

### 4. Itera Basado en Insights

Los KPIs no son estáticos. Si descubres que un peso de complejidad está mal calibrado, ajústalo.

---

## Casos de Uso Reales

### E-commerce B2B
- **Workload**: Complejidad por número de productos en orden
- **3-KPI**: Procesamiento de pedidos
- **Financial**: Márgenes por categoría de producto

### Distribuidores Mayoristas
- **Workload**: Complejidad por líneas de factura
- **3-KPI**: Registro de facturas
- **Financial**: Concentración de proveedores

### Centros de Servicios Compartidos
- **Workload**: Complejidad por número de cuentas contables
- **3-KPI**: Procesamiento de transacciones
- **Financial**: Eficiencia de costos operacionales

---

## Conclusión

**Lo que hace único a este framework:**

1. Nacido de producción real, no de teoría
2. Prioriza confiabilidad sobre comprehensividad
3. Considera contexto, no solo volumen
4. Generalizable a múltiples industrias

**Recuerda:** Un KPI que no puedes defender con 100% de certeza es un KPI que destruye confianza.
