//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
import java.util.*
import kotlin.*
import java.lang.*
private fun CaesarCipher(text:String,key:Int,decryptMode:Boolean): String {
    val newKey=when(decryptMode){
        true -> 26-key
        else -> key
    }
    val textChars=text.toCharArray()
    val ansChars=CharArray(textChars.size)
    for(i in textChars.indices){
        //TIP Press <shortcut actionId="Debug"/> to start debugging your code. We have set one <icon src="AllIcons.Debugger.Db_set_breakpoint"/> breakpoint
        // for you, but you can always add more by pressing <shortcut actionId="ToggleLineBreakpoint"/>.
        if(textChars[i] in 'A'..'Z'){
            ansChars[i] = ((textChars[i].code-'A'.code+newKey)%26+'a'.code).toChar()
        }
        else if(textChars[i] in 'a'..'z'){
            ansChars[i] = ((textChars[i].code-'a'.code+newKey)%26+'A'.code).toChar()
        }
        else{
            ansChars[i]=textChars[i]
        }
    }
    return String(ansChars)
}
private fun main() {
    print("Enter the text to be processed: ")
    //TIP Press <shortcut actionId="ShowIntentionActions"/> with your caret at the highlighted text
    // to see how IntelliJ IDEA suggests fixing it.
    val toBeProcessed:String = readln()
    print("Enter the key: ")
    val key=readln().toInt()
    var flag:Int
    do {
        print("Encrypt (0) or decrypt (1)? Please choose: ")
        flag = readln().toInt()
        if (flag != 0 && flag != 1) {
            print("ERROR: You should input 1 or 0.")
        }
        else break
    }while(true)
    val modeFlag:Boolean=when(flag){
        1->true
        else->false
    }
    val final=CaesarCipher(toBeProcessed,key,modeFlag)
    print(when(modeFlag){
        true->"Decryption "
        else->"Encryption "
    }+"finished. The result is: "+final)
}
