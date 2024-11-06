resource "aws_lambda_function" "example_lambda" {
  filename         = "lambda_function_payload.zip"
  function_name    = "example_lambda"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "index.handler"
  runtime          = "nodejs12.x"
  source_code_hash = filebase64sha256("lambda_function_payload.zip")
}
