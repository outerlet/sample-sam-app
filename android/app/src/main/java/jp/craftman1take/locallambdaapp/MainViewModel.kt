package jp.craftman1take.locallambdaapp

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory

class MainViewModel : ViewModel() {
    private val service = Retrofit.Builder()
        .baseUrl("http://$LOCALSTACK_HOST_IP_ADDRESS:$LOCALSTACK_PORT")
        .addConverterFactory(
            MoshiConverterFactory.create(
                Moshi.Builder().addLast(KotlinJsonAdapterFactory()).build()
            )
        )
        .build()
        .create(LocalStackService::class.java)

    private val _resultText = MutableLiveData("")
    val resultText: LiveData<String> = _resultText

    fun getSimpleResponse(number: Int) {
        viewModelScope.launch(Dispatchers.Default) {
            runCatching {
                service.getSimpleResponse(number)
            }.onSuccess {
                _resultText.postValue(it.message)
            }.onFailure {
                _resultText.postValue("ERROR: ${it.message}")
            }
        }
    }

    companion object {
        // LocalStack が動作しているマシンのIPアドレスを設定
        private const val LOCALSTACK_HOST_IP_ADDRESS = "127.0.0.1"

        // LocalStack がListenしているポート番号を変更している場合は変更
        private const val LOCALSTACK_PORT = 4566
    }
}