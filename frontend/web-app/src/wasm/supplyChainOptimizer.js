/**
 * Supply Chain Optimization Algorithms
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
 * @param {Array} distances - 2D array of distances between locations
 * @param {number} startNode - Starting node index
 * @returns {Object} Object containing optimal route and total distance
 */
export function optimizeRoute(distances, startNode) {
  const n = distances.length;
  if (n === 0) {
    return { route: [], distance: 0 };
  }
  
  // Simple nearest neighbor algorithm (for demonstration)
  const visited = new Array(n).fill(false);
  const route = [startNode];
  visited[startNode] = true;
  
  let current = startNode;
  let totalDistance = 0;
  
  for (let i = 1; i < n; i++) {
    let nearest = -1;
    let minDistance = Infinity;
    
    for (let j = 0; j < n; j++) {
      if (!visited[j] && distances[current][j] < minDistance) {
        minDistance = distances[current][j];
        nearest = j;
      }
    }
    
    if (nearest !== -1) {
      route.push(nearest);
      visited[nearest] = true;
      totalDistance += minDistance;
      current = nearest;
    }
  }
  
  // Return to start
  totalDistance += distances[current][startNode];
  route.push(startNode);
  
  return { route, distance: totalDistance };
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
  const weights = {
    deliveryTime: 0.3,
    quality: 0.3,
    financial: 0.25,
    compliance: 0.15
  };
  
  const weightedScore = (
    deliveryTimeScore * weights.deliveryTime +
    qualityScore * weights.quality +
    financialStability * weights.financial +
    complianceScore * weights.compliance
  );
  
  return Math.min(100, Math.max(0, weightedScore)); // Clamp between 0 and 100
}

// Example usage:
// const eoq = calculateEOQ(10000, 50, 2);
// console.log('Optimal EOQ:', eoq);
// 
// const distances = [
//   [0, 10, 15, 20],
//   [10, 0, 35, 25],
//   [15, 35, 0, 30],
//   [20, 25, 30, 0]
// ];
// const result = optimizeRoute(distances, 0);
// console.log('Optimal route:', result.route);
// console.log('Total distance:', result.distance);