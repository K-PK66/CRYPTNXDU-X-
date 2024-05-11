//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
import kotlin.*

private fun caesarCipher(text:String, key:Int, decryptMode:Boolean): String {
    val newKey=when(decryptMode){
        true -> 26-key
        else -> key
    }
    val textChars=text.toCharArray()
    val ansChars=CharArray(textChars.size)
    for(i in textChars.indices){
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
    val final=caesarCipher(toBeProcessed,key,modeFlag)
    print(when(modeFlag){
        true->"Decryption "
        else->"Encryption "
    }+"finished. The result is: "+final)
}
