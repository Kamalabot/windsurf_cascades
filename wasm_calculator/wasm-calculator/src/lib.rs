mod calculator;

use wasm_bindgen::prelude::*;

// Export the Calculator type
pub use calculator::Calculator;

#[wasm_bindgen]
pub fn init_wasm() -> Result<(), JsValue> {
    #[cfg(feature = "console_error_panic_hook")]
    console_error_panic_hook::set_once();
    Ok(())
}

pub fn add(left: u64, right: u64) -> u64 {
    left + right
}
