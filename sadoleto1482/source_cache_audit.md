# Source cache audit and the R1102 catalogue lead

20 September 2026. Status: in progress.

The earlier local image cache did not contain every image listed in the
cached Vestigia metadata. It is therefore unsafe to equate inspecting the
local files with inspecting all catalogued images.

## R1102: legacy note

Vestigia 1286, `props.document.import_raw.megjegyzesek`, states:

> A levél rejtjeles részeinek beragasztott és mellékelt lapokon olvasható a feloldása.

Working translation: the decipherment of the letter's encrypted portions can
be read on pasted-in and attached sheets. The current `comment` field is null;
the information survives in the legacy import field.

This is **catalogue testimony that decipherment sheets exist**, not a
transcription of those sheets or proof of their completeness. It materially
qualifies the earlier assumption that R1102 lacks any prior decipherment.
The possible interlinear notes on page 4 are separate visible evidence.

## Missing images retrieved

`fetch_missing_r1102.py` retrieved these three public images using their URLs
in `vestigia/v1286.json`. A sandbox network denial was followed by an approved
escalated retry; all three downloads completed.

- `HU_MNL_OL_X_10891_DF_294367_0001.jpg`
- `HU_MNL_OL_X_10891_DF_294367_0002.JPG`
- `HU_MNL_OL_X_10891_DF_294367_0003.JPG`

They are cached under `img/v/v1286_mnl_...`. Review views are
`img/mnl1102_0.jpg` through `img/mnl1102_2.jpg`.

Visual inspection shows the first page, the page-2/page-3 spread, and the
final page, respectively. They do not visibly supply a separate plaintext
slip. The final-page view includes the address and folded/pasted paper area
below the writing; no full decipherment was recovered from that area here.
The metadata's linked attachment is Vestigia 1287, a different letter dated
28 June, not an identified decipherment of the July cipher.

Thus the catalogue lead remains unresolved. Do not report the decipherment
sheets as absent, but do not treat an unseen sheet as evidence for a particular
reading, the original title, or X's exact lexical expansion.

## Other cache gaps found

Comparing file names in cached metadata against local image names also found:

| Record | Not yet cached at this audit |
|---|---|
| 1283, R1101 clear witness 7a | Two `HU_MNL_OL_X_10891_DF_294364_000*.jpg/JPG` images |
| 1284, R1101 original | Three `HU_MNL_OL_X_10891_DF_294364_a_000*.jpg/JPG` images |
| 1318, R1106 original | Three `HU_MNL_OL_X_10891_DF_294396_000*.jpg/JPG` images |
| 1319, R1106 witness 26a | `1387657541.jpg` |

No missing file names were found for 1294 (R1103), 1286 after the new download,
or 4004 (26b). This is a filename audit against the cached metadata, not a
guarantee that the archive has digitised every relevant sheet.

## Follow-up: the nine remaining files are now cached

`fetch_remaining_images.py` downloaded all nine files listed above after an
approved retry for the sandbox network denial. A contact sheet,
`img/additional_sources.jpg`, was inspected. Each new file matches the page
arrangement of an existing source, including the lifted-slip view of R1106
and the same two-paragraph 26a card. No new written surface was identified.

`additional_image_comparison.json` records the closest existing file for each
download, comparing RGB images resized to 540 × 405. Mean absolute differences
are 0.2406–0.2769 for the eight Hungarian-archive files and 0.5300 for the
additional 26a JPEG, on the 0–255 channel scale. Together with their matching
geometry, these small differences support treating them as alternative
encodings of the already reviewed views, not independent exposures revealing
new strokes. This does not establish archive provenance from pixels alone.

The gaps in the table are therefore **closed as cache gaps**, not as gaps in
decipherment. The corpus now contains every image filename listed in the
cached metadata for 1283, 1284, 1286, 1294, 1318, 1319 and 4004. Unphotographed
or unlinked sheets, including those reported for R1102, remain an open question.

## DECODE cookie verification

Following the user's reminder, `audit_decode_access.py` requested all four
DECODE record pages and their Documents, Associated Records, and Images
management listings with the existing cookie from `bordeaux/decode/cookie.txt`.
No cookie value is copied into these research notes or the audit output.

The public record pages were readable and listed the already cached image
names. All twelve management-listing requests redirected to login. The
`no_records_reported` booleans in `decode_access_audit.json` reflect generic
page text and **must not be interpreted as evidence of empty attachment
lists** when the page is a login response.

A separate `--image-test` request to the full-size image server succeeded:
20,021,629 bytes, `image/png`, no forbidden response, and SHA-256 equality
with cached `IMG_R1101_I5655_P2.png`. The result is recorded in
`decode_image_access_test.json`. Thus the saved cookie is usable on the
image server even though it did not authenticate the web management listings.
It would be incorrect to describe it as wholly expired or rejected.

Full-size image access is therefore available. The authenticated attachment
listing audit remains incomplete; the redirects say nothing about whether
additional decipherment files exist there.

### Credential-component audit

Local inspection on 20 September identified separate `dc-session`,
`PHPSESSID`, and web-app JWT components in the saved cookie. Only their
names and expiration metadata were examined; no credential values are
included in research outputs.

The cookie's `decryptweb23[JWT]` payload reports expiry at
**2026-09-18 20:13:44 UTC**. The separate `decode/jwt.txt` token is different
and reports expiry at **2026-09-19 12:55:26 UTC**. Both dates precede this
audit. These are locally decoded claims, not a signature validation or a
test of the remaining server-side session cookies.

The credential-free result is `decode_credential_metadata.json`. This
qualifies the access diagnosis: the saved *web-app token* is expired, while
the successful image request proves that the saved credential bundle still
permits image access. Expiry is consistent with the management redirects
but does not prove it is their sole cause. Repeating the same listing
requests with the unchanged bundle is unlikely to add evidence. A refreshed
authorized web session would be needed to retry that access route usefully;
cached manuscripts remain available for continuing the decipherment.
