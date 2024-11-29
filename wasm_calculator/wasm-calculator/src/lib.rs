use wasm_bindgen::prelude::*;

mod calculator;
pub use calculator::Calculator;

#[wasm_bindgen(start)]
pub fn init_wasm() {
    #[cfg(feature = "console_error_panic_hook")]
    console_error_panic_hook::set_once();
}
