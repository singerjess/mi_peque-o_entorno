FROM scipoptsuite/scipoptsuite:7.0.2-teach

EXPOSE 9001
COPY test_cases /test_cases
VOLUME /test_cases