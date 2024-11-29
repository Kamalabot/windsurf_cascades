/* tslint:disable */
/* eslint-disable */
export function init_wasm(): void;
export class Calculator {
  free(): void;
  constructor();
  /**
   * @param {number} value
   * @returns {number}
   */
  add(value: number): number;
  /**
   * @param {number} value
   * @returns {number}
   */
  subtract(value: number): number;
  /**
   * @param {number} value
   * @returns {number}
   */
  multiply(value: number): number;
  /**
   * @param {number} value
   * @returns {number}
   */
  divide(value: number): number;
  /**
   * @param {number} value
   * @returns {number}
   */
  sin(value: number): number;
  /**
   * @param {number} value
   * @returns {number}
   */
  cos(value: number): number;
  /**
   * @param {number} value
   * @returns {number}
   */
  tan(value: number): number;
  memory_store(): void;
  /**
   * @returns {number}
   */
  memory_recall(): number;
  memory_clear(): void;
  memory_add(): void;
  memory_subtract(): void;
  clear(): void;
  toggle_angle_mode(): void;
  /**
   * @returns {number}
   */
  get_current_value(): number;
  /**
   * @param {number} value
   */
  set_value(value: number): void;
  /**
   * @returns {number}
   */
  equals(): number;
}
