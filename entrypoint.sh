#!/bin/sh

CMD=$*
pulumi login "s3://${PULUMI_STATE_BUCKET}"
if [ "${PULUMI_STACK+z}" != z ]; then
    echo "Pulumi stack is unset. Will not be selecting a stack."
else
    pulumi stack select "${PULUMI_STACK}"
fi

# shellcheck disable=SC2086
pulumi ${CMD}
