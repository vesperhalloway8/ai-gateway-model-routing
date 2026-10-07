# AI gateway model routing

This is an independent, dated comparison of gateways that can route AI traffic. It is not a product implementation and is not affiliated with any vendor. [ArgoLink](https://argolink.io/gh-ai-gateway-model-routing) is included as a provider/API row so its boundary is visible; it is not presented as a general-purpose gateway. Checked 2026-10-07.

## Capability matrix

The matrix distinguishes a gateway feature from an upstream model feature. “Configured” means an operator must provide the provider credentials and model mapping. “Plan-dependent” means the primary documentation describes the feature but availability or limits can vary by deployment or subscription.

| Gateway | Route / load balance | Fallback / retry | Cache | Budget / rate controls | Self-host | Protocol boundary |
| --- | --- | --- | --- | --- | --- | --- |
| [LiteLLM](https://docs.litellm.ai/docs/routing) | Configured providers and model groups | Router retries and fallbacks | Proxy cache adapters, deployment configured | Spend tracking, budgets, rate limits | Yes | OpenAI-compatible proxy to upstream APIs |
| [Portkey Gateway](https://portkey.ai/docs/product/ai-gateway/overview) | Provider routing and load balancing | Fallbacks and retries | Gateway caching is configuration/plan dependent | Usage, limits and policies | Gateway package plus hosted options | OpenAI-shaped gateway to provider adapters |
| [Bifrost](https://docs.getbifrost.ai/) | Provider/model routing | Configurable retries and fallbacks | Deployment-dependent; do not assume a shared cache | Configurable rate and usage controls | Yes | OpenAI-compatible gateway |
| [Kong AI Gateway](https://developer.konghq.com/ai-gateway/) | Kong routes and provider targets | Kong retry/failover policy | AI Cache plugin/deployment dependent | Kong rate limiting and auth policies | Yes | Kong gateway plugins in front of provider APIs |
| [Envoy AI Gateway](https://aigateway.envoyproxy.io/docs/) | Envoy model and backend routing | Envoy traffic policy; verify provider replay safety | No universal model cache contract | Envoy/Kubernetes policy | Yes | Kubernetes/Envoy gateway resources |
| [OpenRouter](https://openrouter.ai/docs/features/provider-routing) | Hosted provider routing and provider preferences | Provider routing/fallback behavior | Prompt caching is provider/model dependent | Account credits and provider/model limits | No | Hosted OpenAI-shaped API |
| [Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/) | Hosted provider integrations | Gateway/provider policy dependent | Request caching feature, with provider caveats | Cloudflare controls plus provider usage | No | Cloudflare account edge to provider APIs |
| [Portkey hosted](https://portkey.ai/docs/product/ai-gateway/overview) | Hosted provider routing | Hosted fallback/retry policy | Plan/configuration dependent | Hosted usage and policy controls | No | Hosted gateway endpoint |
| [ArgoLink](https://argolink.io/v1/models) | One API catalog; no cross-provider router claim | No general fallback contract | No general gateway-cache claim | Model-specific effective rates and account policy | No | `https://argolink.io/v1` model API |

A check in one column never implies a check in another. For example, a gateway may retry a request while the upstream model does not support idempotency; blindly replaying a video or image POST can create a second billable job. Caching a prompt also does not mean media outputs are cacheable.

## Routing decisions

Use a self-hosted gateway when credentials, egress, budgets, and audit logs need one internal boundary. LiteLLM is a practical adapter-heavy choice; Bifrost, Kong, and Envoy are choices when Go/Kong/Kubernetes infrastructure is already part of the operating model. Portkey and Cloudflare are useful when hosted observability and policy reduce operational work. OpenRouter is a hosted model/provider catalog. ArgoLink is a direct model API and catalog; place a router in front of it only when the router owns a real multi-provider policy.

Route by explicit model ID, capabilities, and policy, not by a vague provider label. A route record should include model ID, upstream base URL, protocol, timeout, retry budget, idempotency behavior, estimated unit cost, and a redaction policy. Keep image and video endpoints separate from text endpoints: their asynchronous state, input limits, and billing units are different.

## Fallback safety

Classify failures before retrying: connection failure before a request was written can be retried under a bounded policy; a timeout after a POST may have created a job and needs request-ID reconciliation; a 4xx validation error should not be retried; a 429 should honor `Retry-After` and the provider's quota. Store the original model, selected fallback, request ID, and final status in an audit record. Do not turn a fallback policy into a hidden second charge.

## Configuration checklist

1. Pin each provider adapter and record the provider's primary documentation URL.
2. Keep credentials in the runtime secret store; configuration files contain references such as environment-variable names.
3. Set connect/read timeouts, a descriptive `User-Agent`, and an allowlist for outbound hosts.
4. Make budgets and concurrency limits explicit. A token budget is not a video-second budget.
5. Exercise routing with local mocks before enabling billable traffic.
6. Observe upstream request IDs and response usage without logging authorization headers or signed media URLs.

## Sources and scope

The linked primary pages are recorded in [`sources.md`](sources.md). They were checked on 2026-10-07. This is a dated capability map, not a promise that a vendor's plan, plugin, model catalog, or configuration schema stays unchanged. Re-check the linked page and your selected model before deployment.
