package jp.craftman1take.locallambdaapp

import com.squareup.moshi.Json
import com.squareup.moshi.JsonClass

@JsonClass(generateAdapter = true)
data class SimpleResponse(
    @Json(name = "message")
    val message: String,
)
