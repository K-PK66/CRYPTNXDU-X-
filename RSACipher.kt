import kotlin.random.Random

private fun euclid4GCDPlus(a: Int, b: Int): Triple<Int, Int, Int> {
    return if (b == 0) {
        Triple(1, 0, a)
    } else {
        val (x, y, euclidResult) = euclid4GCDPlus(b, a % b)
        Triple(y, x - (a / b) * y, euclidResult)
    }
}

private fun euclid4GCD(a: Int, b: Int): Int {
    return if (a % b == 0) {
        b
    } else {
        euclid4GCD(b, a % b)
    }
}

private fun montgomeryModularMultiplication4Mod(base: Int, exponent: Int, n: Int): Int {
    val binArray = exponent.toString(2).reversed().toCharArray()
    val r = binArray.size
    val baseArray = mutableListOf<Int>()
    var preBase = base
    baseArray.add(preBase)
    for (i in 0..<r - 1) {
        val nextBase = (preBase * preBase) % n
        baseArray.add(nextBase)
        preBase = nextBase
    }
    var result = 1
    for (i in binArray.indices) {
        if (binArray[i] == '1') {
            result *= baseArray[i]
            result %= n
        }
    }
    return result
}

private fun keyPairGenerator(p: Int, q: Int): Pair<Pair<Int, Int>, Pair<Int, Int>> {
    val n = p * q
    val phi = (p - 1) * (q - 1)
    //Private key
    var prK = Random.nextInt(2, phi)
    //Public key
    var puK = 0
    while (puK == 0) {
        if (euclid4GCD(prK, phi) == 1) {
            puK = euclid4GCDPlus(prK, phi).first % phi
        } else {
            prK = Random.nextInt(2, phi)
        }
    }
    return Pair(Pair(n, prK), Pair(n, puK))
}

private fun isPrime(n: Int): Boolean {
    if (n <= 1) {
        return false
    }
    for (i in 2..n / 2) {
        if (n % i == 0) {
            return false
        }
    }
    return true
}

private class RSACipher(keyPair: Pair<Int, Int>) {
    val n = keyPair.first
    val key = keyPair.second
    fun encrypt(c: List<Int>): List<Int> {
        return c.map { montgomeryModularMultiplication4Mod(it, key, n) }
    }

    fun decrypt(e: List<Int>): List<Int> {
        return e.map { montgomeryModularMultiplication4Mod(it, key, n) }
    }
}

private fun encode2Integer(text: String): List<Int> {
    return text.map { it.code }
}

private fun decode2Character(list: List<Int>): String {
    return list.map { it.toChar() }.joinToString("")
}

private fun randomPrimeGenerator(x: Int): Int {
    val newNum = Random.nextInt(x)
    return if (isPrime(newNum)) {
        newNum
    } else {
        randomPrimeGenerator(x)
    }
}

private fun main() {
    //Prime Number Prompt
    println("Please select 2 PRIME numbers for key pair generation.")
    print("First PRIME number: ")
    var p = readln().toInt()
    print("Second PRIME number: ")
    var q = readln().toInt()
    println("Confirmed. p = $p, q = $q")
    //Prime check
    println("Checking whether p & q are PRIME...")
    if (isPrime(p) && isPrime(q)) {
        println("Checked: BOTH PRIME")
    } else if (isPrime(q)) {
        println("Checked: p is NOT PRIME")
        p = randomPrimeGenerator(p)
        println("Correction：p has been changed to be a PRIME.")
    } else if (isPrime(p)) {
        println("Checked: q is NOT PRIME")
        q = randomPrimeGenerator(q)
        println("Correction: q has been changed to be a PRIME.")
    } else {
        println("Checked: NO PRIMES")
        p = randomPrimeGenerator(p)
        q = randomPrimeGenerator(q)
        println("Correction: p and q has been changed to be PRIME.")
    }
    println("Check finished. (p = $p, q = $q)")
    val (privateKeyPair, publicKeyPair) = keyPairGenerator(p, q)
    val encryptService = RSACipher(privateKeyPair)
    val decryptService = RSACipher(publicKeyPair)
    print("Enter text to be processed: ")
    val message = readln()
    println("Gotcha. Transcode in progress.")
    Thread.sleep(1000)
    val transcodeText = encode2Integer(message)
    println("Transcode finished: $transcodeText")
    println("Encryption in progress.")
    Thread.sleep(1000)
    val encryptedCodeList = encryptService.encrypt(transcodeText)
    println("Encryption done: $encryptedCodeList")
    val decodedEncrypt = decode2Character(encryptedCodeList)
    println("Which can be translated into text: $decodedEncrypt")
    println("Decryption in progress.")
    val decryptedCodeList = decryptService.decrypt(encryptedCodeList)
    println("Decryption done: $decryptedCodeList")
    val decodedDecrypt = decode2Character(decryptedCodeList)
    println("Decryption done: $decodedDecrypt")
    println("(Private Key Pair: $privateKeyPair, Public Key Pair: $publicKeyPair)")
}