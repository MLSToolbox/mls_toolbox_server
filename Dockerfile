FROM python:3.10-alpine

WORKDIR /app



COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app

ENV MLS_CODE_GENERATOR_URI="mls_code_generator"
ENV MLS_CODE_GENERATOR_PORT="5050"

ENV MLS_CODE_ASSESS_URI="mls_toolbox_code_assessment"
ENV MLS_CODE_ASSESS_PORT="5060"

ENV EXECUTION_MODE="prod"
ENV FLASK_ENV="production"
ENV CORS_ORIGINS="*"
ENV LOG_LEVEL="INFO"



ENTRYPOINT ["python3"]
CMD ["server.py"]