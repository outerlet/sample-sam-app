package jp.craftman1take.locallambdaapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.livedata.observeAsState
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.constraintlayout.compose.ConstraintLayout
import androidx.constraintlayout.compose.Dimension
import jp.craftman1take.locallambdaapp.ui.theme.LocalLambdaAppTheme

class MainActivity : ComponentActivity() {
    private val viewModel by viewModels<MainViewModel>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            LocalLambdaAppTheme {
                Content(
                    modifier = Modifier.fillMaxSize(),
                    resultText = viewModel.resultText.observeAsState(initial = "").value,
                    onSubmit = { inputValue ->
                        inputValue.toIntOrNull()?.let {
                            viewModel.getSimpleResponse(it)
                        }
                    }
                )
            }
        }
    }
}

@Composable
@OptIn(ExperimentalMaterial3Api::class)
fun Content(
    modifier: Modifier = Modifier,
    resultText: String = "Initial Value",
    onSubmit: (String) -> Unit = {},
) {
    Scaffold(
        modifier = modifier,
        topBar = {
            TopAppBar(
                title = { Text(text = "SimpleResponseFunction") },
                colors = TopAppBarDefaults.topAppBarColors(
                    titleContentColor = Color.White,
                    containerColor = Color.Blue,
                )
            )
        }
    ) { innerPadding ->
        ConstraintLayout(modifier = Modifier
            .fillMaxSize()
            .padding(innerPadding)) {
            val currentInput = remember { mutableStateOf("") }
            val (inputRef, textRef, buttonRef) = createRefs()

            OutlinedTextField(
                modifier = Modifier.constrainAs(inputRef) {
                    width = Dimension.fillToConstraints
                    height = Dimension.wrapContent
                    top.linkTo(parent.top, margin = 12.dp)
                    start.linkTo(parent.start, margin = 12.dp)
                    end.linkTo(parent.end, margin = 12.dp)
                },
                value = currentInput.value,
                onValueChange = { currentInput.value = it },
            )

            Text(
                modifier = Modifier.constrainAs(textRef) {
                    width = Dimension.wrapContent
                    height = Dimension.wrapContent
                    top.linkTo(inputRef.bottom)
                    bottom.linkTo(buttonRef.top)
                    centerHorizontallyTo(parent)
                },
                fontSize = 20.sp,
                text = resultText,
            )

            Button(
                modifier = Modifier.constrainAs(buttonRef) {
                    width = Dimension.fillToConstraints
                    height = Dimension.wrapContent
                    bottom.linkTo(parent.bottom, margin = 12.dp)
                    start.linkTo(parent.start, margin = 12.dp)
                    end.linkTo(parent.end, margin = 12.dp)
                },
                onClick = { onSubmit(currentInput.value) },
            ) {
                Text(text = "CLICK ME")
            }
        }
    }
}

@Composable
@Preview(showBackground = true)
fun ContentPreview() {
    Content(modifier = Modifier.fillMaxSize())
}
