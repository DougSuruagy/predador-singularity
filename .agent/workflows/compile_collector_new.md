# Workflow to compile COLLECTOR_NEW.mq5

---
description: Compile the COLLECTOR_NEW.mq5 file using MetaEditor CLI
---

1. Open MetaEditor (ensure MetaTrader 5 is installed).
2. Use the command line to compile the file:
   ```
   MetaEditor64.exe /compile:"c:\\Users\\Douglas\\tryd\\COLLECTOR_NEW.mq5" /log
   ```
3. Check the output log for any compilation errors.
4. If errors appear, open the file in MetaEditor, fix them, and repeat step 2.
5. Once compilation succeeds, the compiled `.ex5` will be placed in the same directory.

**Note**: This workflow assumes MetaEditor is in the system PATH. Adjust the path to MetaEditor64.exe if necessary.
