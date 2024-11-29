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
   * @returns {number}
   */
  equals(): number;
  clear(): void;
  /**
   * @returns {number}
   */
  get_current_value(): number;
  /**
   * @param {number} value
   */
  set_value(value: number): void;
  memory_store(): void;
  /**
   * @returns {number}
   */
  memory_recall(): number;
  memory_clear(): void;
  memory_add(): void;
  memory_subtract(): void;
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
  toggle_angle_mode(): void;
}

export type InitInput = RequestInfo | URL | Response | BufferSource | WebAssembly.Module;

export interface InitOutput {
  readonly memory: WebAssembly.Memory;
  readonly __wbg_calculator_free: (a: number, b: number) => void;
  readonly calculator_new: () => number;
  readonly calculator_add: (a: number, b: number) => number;
  readonly calculator_subtract: (a: number, b: number) => number;
  readonly calculator_multiply: (a: number, b: number) => number;
  readonly calculator_divide: (a: number, b: number, c: number) => void;
  readonly calculator_equals: (a: number) => number;
  readonly calculator_clear: (a: number) => void;
  readonly calculator_get_current_value: (a: number) => number;
  readonly calculator_set_value: (a: number, b: number) => void;
  readonly calculator_memory_store: (a: number) => void;
  readonly calculator_memory_recall: (a: number) => number;
  readonly calculator_memory_clear: (a: number) => void;
  readonly calculator_memory_add: (a: number) => void;
  readonly calculator_memory_subtract: (a: number) => void;
  readonly calculator_sin: (a: number, b: number) => number;
  readonly calculator_cos: (a: number, b: number) => number;
  readonly calculator_tan: (a: number, b: number) => number;
  readonly calculator_toggle_angle_mode: (a: number) => void;
  readonly init_wasm: () => void;
  readonly __wbindgen_add_to_stack_pointer: (a: number) => number;
  readonly __wbindgen_free: (a: number, b: number, c: number) => void;
  readonly __wbindgen_malloc: (a: number, b: number) => number;
  readonly __wbindgen_realloc: (a: number, b: number, c: number, d: number) => number;
  readonly __wbindgen_start: () => void;
}

export type SyncInitInput = BufferSource | WebAssembly.Module;
/**
* Instantiates the given `module`, which can either be bytes or
* a precompiled `WebAssembly.Module`.
*
* @param {{ module: SyncInitInput }} module - Passing `SyncInitInput` directly is deprecated.
*
* @returns {InitOutput}
*/
export function initSync(module: { module: SyncInitInput } | SyncInitInput): InitOutput;

/**
* If `module_or_path` is {RequestInfo} or {URL}, makes a request and
* for everything else, calls `WebAssembly.instantiate` directly.
*
* @param {{ module_or_path: InitInput | Promise<InitInput> }} module_or_path - Passing `InitInput` directly is deprecated.
*
* @returns {Promise<InitOutput>}
*/
export default function __wbg_init (module_or_path?: { module_or_path: InitInput | Promise<InitInput> } | InitInput | Promise<InitInput>): Promise<InitOutput>;
