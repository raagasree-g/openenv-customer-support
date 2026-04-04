export interface InventoryState {
  factory: number;
  warehouse: number;
  retail: number;
}

export interface BacklogState {
  factory: number;
  warehouse: number;
  retail: number;
}

export interface InTransitState {
  toWarehouse: number[];
  toRetail: number[];
}

export interface EnvState {
  inventory: InventoryState;
  backlog: BacklogState;
  inTransit: InTransitState;
  demand: number;
  week: number;
  totalReward: number;
  lastReward: number;
  done: boolean;
}

export interface EnvAction {
  factoryToWH: number;
  whToRetail: number;
}

export interface StepResult {
  state: EnvState;
  reward: number;
  done: boolean;
  info: any;
}

export class LogisticsFlowEnv {
  private inv: [number, number, number] = [100, 50, 20];
  private backlog: [number, number, number] = [0, 0, 0];
  private toWH: number[] = [0, 0]; // 2-week lead time
  private toRetail: number[] = [0, 0];
  private week = 0;
  private totalReward = 0;
  private lastReward = 0;
  private maxWeeks = 52;

  constructor(private config: any = {}) {}

  reset(): EnvState {
    this.inv = [100, 50, 20];
    this.backlog = [0, 0, 0];
    this.toWH = [0, 0];
    this.toRetail = [0, 0];
    this.week = 0;
    this.totalReward = 0;
    this.lastReward = 0;
    return this.state();
  }

  state(): EnvState {
    return {
      inventory: { factory: this.inv[0], warehouse: this.inv[1], retail: this.inv[2] },
      backlog: { factory: this.backlog[0], warehouse: this.backlog[1], retail: this.backlog[2] },
      inTransit: {
        toWarehouse: [...this.toWH],
        toRetail: [...this.toRetail]
      },
      demand: this.generateDemand(),
      week: this.week,
      totalReward: this.totalReward,
      lastReward: this.lastReward,
      done: this.week >= this.maxWeeks
    };
  }

  private generateDemand(): number {
    const base = this.config.demandBase || 15;
    const amplitude = this.config.demandAmplitude || 10;
    const seasonality = Math.sin(this.week * (2 * Math.PI / 52)) * amplitude;
    const noise = (Math.random() - 0.5) * 5;
    return Math.max(0, Math.round(base + seasonality + noise));
  }

  step(action: EnvAction): StepResult {
    const currentDemand = this.generateDemand();
    
    // 1. Receive incoming shipments
    const arrivingAtWH = this.toWH.shift() || 0;
    const arrivingAtRetail = this.toRetail.shift() || 0;
    
    this.inv[1] += arrivingAtWH;
    this.inv[2] += arrivingAtRetail;

    // 2. Fulfill demand at Retail
    const totalRetailDemand = currentDemand + this.backlog[2];
    const fulfilledRetail = Math.min(this.inv[2], totalRetailDemand);
    this.inv[2] -= fulfilledRetail;
    this.backlog[2] = totalRetailDemand - fulfilledRetail;

    // 3. Fulfill orders from WH to Retail
    const totalWHOrder = action.whToRetail + this.backlog[1];
    const shippedToRetail = Math.min(this.inv[1], totalWHOrder);
    this.inv[1] -= shippedToRetail;
    this.backlog[1] = totalWHOrder - shippedToRetail;
    this.toRetail.push(shippedToRetail);

    // 4. Fulfill orders from Factory to WH
    const totalFactoryOrder = action.factoryToWH + this.backlog[0];
    const shippedToWH = totalFactoryOrder; 
    this.backlog[0] = 0;
    this.toWH.push(shippedToWH);

    // 5. Factory Production
    this.inv[0] = Math.min(200, this.inv[0] + 30);

    // 6. Calculate Reward
    const revenue = fulfilledRetail * 5.0;
    const hCost = (this.inv[0] + this.inv[1] + this.inv[2]) * 0.5;
    const bCost = (this.backlog[0] + this.backlog[1] + this.backlog[2]) * 1.0;
    const reward = revenue - (hCost + bCost);

    // 7. Update State
    this.week++;
    this.totalReward += reward;
    this.lastReward = reward;
    
    if (this.week >= this.maxWeeks) {
      return { state: this.state(), reward, done: true, info: {} };
    }

    return {
      state: this.state(),
      reward,
      done: false,
      info: {
        revenue,
        holdingCosts: hCost,
        backlogCosts: bCost
      }
    };
  }
}
