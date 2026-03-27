import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;

public class RiskScanner extends GhidraScript {
    @Override
    public void run() throws Exception {
        println("\n--- [AI-ZeroDay] Starting Static Risk Scan ---");
        
        FunctionIterator iter = currentProgram.getFunctionManager().getFunctions(true);
        while (iter.hasNext() && !monitor.isCancelled()) {
            Function f = iter.next();
            if (f.getName().contains("strcpy")) {
                println("[ALERT] Dangerous Function Found: " + f.getName() + " at " + f.getEntryPoint());
            }
        }
        println("--- [AI-ZeroDay] Scan Complete ---\n");
    }
}
