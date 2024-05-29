import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.IvParameterSpec
import kotlin.*

private fun AESKeyGenerator(size:Int):SecretKey{
    val keyGenerator= KeyGenerator.getInstance("AES")
    keyGenerator.init(size)
    return keyGenerator.generateKey()
}
private fun DESKeyGenerator(size:Int):SecretKey{
    val keyGenerator= KeyGenerator.getInstance("DES")
    keyGenerator.init(size)
    return keyGenerator.generateKey()
}
private fun symmetricKeyCipher(data:ByteArray, key:SecretKey, decryptModeFlag:Boolean, desModeFlag:Boolean):ByteArray{
    val sample=when(desModeFlag){
        false->"AES/CBC/PKCS5Padding"
        else-> "DES"
    }
    val cipher=Cipher.getInstance(sample)
    if(!desModeFlag) {
        val ivParameterSpec = IvParameterSpec(ByteArray(16))
        if (decryptModeFlag) {
            cipher.init(Cipher.DECRYPT_MODE, key, ivParameterSpec)
        } else {
            cipher.init(Cipher.ENCRYPT_MODE, key, ivParameterSpec)
        }
    }
    else{
        if(decryptModeFlag){
            cipher.init(Cipher.DECRYPT_MODE, key)
        }
        else{
            cipher.init(Cipher.ENCRYPT_MODE, key)
        }
    }
    return cipher.doFinal(data)
}
private fun main(){
    print("Enter the text to be processed: ")
    val toBeProcessed = readln()
    var keyLen:Int
    val myKey:SecretKey
    print("AES (0) or DES (1)? Your choice: ")
    val modeValue= readln().toInt()
    if (modeValue==0) do {
        print("Enter the length of the key you want (128/192/256): ")
        keyLen = readln().toInt()
        if(keyLen != 128 && keyLen != 192 && keyLen != 256){
            println("ERROR: the length of the key should be 128 or 192 or 256. Please retry.")
        }
        else break
    }while(true)
    else keyLen=56
    myKey = when(modeValue){
        0->AESKeyGenerator(keyLen)
        else->DESKeyGenerator(keyLen)
    }
    val modeFlag=when(modeValue){
        0->false
        else->true
    }
    println("Key generated. Your key: $myKey")
    Thread.sleep(2000)
    val encryptedData=symmetricKeyCipher(toBeProcessed.toByteArray(),myKey,false,modeFlag)
    println("Encryption complete. Result after encryption: ${encryptedData.contentToString()}")
    Thread.sleep(5000)
    val decryptedData=symmetricKeyCipher(encryptedData,myKey,true,modeFlag)
    println("Decryption complete. Result after decryption: ${decryptedData.contentToString()}")
    println("Which can be transcode as: ${String(decryptedData)}")
}
