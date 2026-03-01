/**
 * Supply Chain Optimization Algorithms - WebAssembly Version
 * 
 * This module contains performance-critical algorithms for supply chain optimization
 * that can be compiled to WebAssembly for better performance.
 */

/**
 * Calculate optimal inventory levels using Economic Order Quantity (EOQ) model
 * @param {number} demand - Annual demand
 * @param {number} orderingCost - Cost per order
 * @param {number} holdingCost - Annual holding cost per unit
 * @returns {number} Optimal order quantity
 */
export function calculateEOQ(demand, orderingCost, holdingCost) {
  if (holdingCost <= 0) {
    throw new Error('Holding cost must be greater than zero');
  }
  
  return Math.sqrt((2 * demand * orderingCost) / holdingCost);
}

/**
 * Calculate total inventory cost
 * @param {number} demand - Annual demand
 * @param {number} orderQuantity - Order quantity
 * @param {number} orderingCost - Cost per order
 * @param {number} holdingCost - Annual holding cost per unit
 * @returns {number} Total inventory cost
 */
export function calculateTotalCost(demand, orderQuantity, orderingCost, holdingCost) {
  if (orderQuantity <= 0) {
    throw new Error('Order quantity must be greater than zero');
  }
  
  const orderingCostTotal = (demand / orderQuantity) * orderingCost;
  const holdingCostTotal = (orderQuantity / 2) * holdingCost;
  
  return orderingCostTotal + holdingCostTotal;
}

/**
 * Optimize supply chain routes using a simplified algorithm
 * @param {Float64Array} distances - 1D array of distances (flattened 2D matrix)
 * @param {number} n - Number of nodes
 * @param {number} startNode - Starting node index
 * @returns {number} Total distance of optimized route
 */
export function optimizeRoute(distances, n, startNode) {
  if (n === 0) {
    return 0;
  }
  
  // Simple nearest neighbor algorithm (for demonstration)
  const visited = new Array(n);
  for (let i = 0; i < n; i++) {
    visited[i] = false;
  }
  
  visited[startNode] = true;
  
  let current = startNode;
  let totalDistance = 0;
  
  for (let i = 1; i < n; i++) {
    let nearest = -1;
    let minDistance = Infinity;
    
    for (let j = 0; j < n; j++) {
      if (!visited[j]) {
        const distance = distances[current * n + j];
        if (distance < minDistance) {
          minDistance = distance;
          nearest = j;
        }
      }
    }
    
    if (nearest !== -1) {
      visited[nearest] = true;
      totalDistance += minDistance;
      current = nearest;
    }
  }
  
  // Return to start
  totalDistance += distances[current * n + startNode];
  
  return totalDistance;
}

/**
 * Calculate supplier risk score based on multiple factors
 * @param {number} deliveryTimeScore - Score for delivery time (0-100)
 * @param {number} qualityScore - Score for quality (0-100)
 * @param {number} financialStability - Score for financial stability (0-100)
 * @param {number} complianceScore - Score for compliance (0-100)
 * @returns {number} Overall risk score (0-100)
 */
export function calculateSupplierRisk(
  deliveryTimeScore,
  qualityScore,
  financialStability,
  complianceScore
) {
  // Weighted average (weights can be adjusted based on business priorities)
  const deliveryTimeWeight = 0.3;
  const qualityWeight = 0.3;
  const financialWeight = 0.25;
  const complianceWeight = 0.15;
  
  const weightedScore = (
    deliveryTimeScore * deliveryTimeWeight +
    qualityScore * qualityWeight +
    financialStability * financialWeight +
    complianceScore * complianceWeight
  );
  
  // Clamp between 0 and 100
  return Math.min(100, Math.max(0, weightedScore));
}