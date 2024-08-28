package jp.craftman1take.locallambdaapp

import retrofit2.http.GET
import retrofit2.http.Query

interface LocalStackService {
    @GET("restapis/$REST_API_ID/simple_response/_user_request_/simple_response")
    suspend fun getSimpleResponse(@Query("number") number: Int): SimpleResponse

    companion object {
        // awslocal apigateway get-rest-apis で確認できる REST API ID をセット
        private const val REST_API_ID = "xxxxxxxxxx"
    }
}