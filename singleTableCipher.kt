import kotlin.*
private val encryptSheet= IntArray(30)
private val decryptSheet= IntArray(30)
private fun sheetReferenceForIndex(c:Char):Int{
    if (c in 'a'..'z') return c.code-'a'.code
    return if (c in 'A'..'Z') c.code-'A'.code
    else -1
}
private fun singleTableCipher(text:String,key:String,decryptMode:Boolean):String{
    val flags=IntArray(30){_->0}
    var k=0
    for(i in key.indices){
        var n = sheetReferenceForIndex(key[i])
        if(flags[n] == 0){
            encryptSheet[k++]=n
            decryptSheet[n]=k-1
            flags[n]=1
        }
    }
    for(i in 0..<26){
        if(flags[i] == 0){
            encryptSheet[k++]=i
            decryptSheet[i]=k-1
        }
    }
    val textLen=text.length
    val ansChars=CharArray(textLen)
    for(i in text.indices){
        if(text[i] in 'a' .. 'z') ansChars[i] = (when(decryptMode){
            true->decryptSheet[text[i].code-'a'.code]
            else->encryptSheet[text[i].code-'a'.code]
        }+'a'.code).toChar()
        else if(text[i] in 'A'..'Z') ansChars[i]=(when(decryptMode){
            true->decryptSheet[text[i].code-'A'.code]
            else->encryptSheet[text[i].code-'A'.code]
        }+'A'.code).toChar()
        else ansChars[i]=text[i]
    }
    return String(ansChars)
}
private fun main(){
    print("Enter the text to be processed: ")
    val toBeProcessed= readln()
    print("Success. Enter your key: ")
    val myKey = readln()
    print("Encrypt (0) or Decrypt (1)? Your choice: ")
    val modeFlag=when(readln().toInt()){
        0->false
        else->true
    }
    print(when(modeFlag){
        true->"De"
        else->"En"
    }+"cryption finished. Result is: ${singleTableCipher(toBeProcessed,myKey,modeFlag)}")
}
