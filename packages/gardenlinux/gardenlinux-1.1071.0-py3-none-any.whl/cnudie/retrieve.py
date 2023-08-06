import functools
import logging

import gci.componentmodel as cm

import ccc.delivery
import delivery.client
import product.v2

logger = logging.getLogger(__name__)


def component_descriptor(
    name: str,
    version: str,
    ctx_repo_url: str,
    delivery_client: delivery.client.DeliveryServiceClient=None,
    cache_dir: str=None,
    validation_mode: cm.ValidationMode=cm.ValidationMode.NONE,
) -> cm.ComponentDescriptor:
    '''
    retrieves the requested, deserialised component-descriptor, preferring delivery-service,
    with a fallback to the underlying oci-registry
    '''
    return _component_descriptor(
        name=name,
        version=version,
        ctx_repo_url=ctx_repo_url,
        delivery_client=delivery_client,
        cache_dir=cache_dir,
        validation_mode=validation_mode,
    )


@functools.lru_cache(maxsize=2048)
def _component_descriptor(
    name: str,
    version: str,
    ctx_repo_url: str,
    delivery_client: delivery.client.DeliveryServiceClient=None,
    cache_dir=None,
    validation_mode=cm.ValidationMode.NONE,
):
    if not delivery_client:
        delivery_client = ccc.delivery.default_client_if_available()

    try:
        return delivery_client.component_descriptor(
            name=name,
            version=version,
            ctx_repo_url=ctx_repo_url,
        )
    except:
        pass

    # fallback to resolving from oci-registry
    if delivery_client:
        logger.warning(f'{name=} {version=} {ctx_repo_url=} - falling back to oci-registry')

    return product.v2.download_component_descriptor_v2(
        component_name=name,
        component_version=version,
        ctx_repo_base_url=ctx_repo_url,
        cache_dir=cache_dir,
        validation_mode=validation_mode,
    )
