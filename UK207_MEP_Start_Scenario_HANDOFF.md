# UK207 — MEP Start Scenario: Session Handoff

**Last updated:** 07.10.2026
**Branch:** `claude/uk207-temel-aktiviteleri-1561f9`
**PR:** https://github.com/erdiakkus/erdiakkus/pull/1 (draft, mergeable, no CI, no review comments)

Notes are in Turkish and English. The programme content is in UK English, per the project's standing instruction.

---

## 1. Amaç

Project Management bir soru sordu: kritik MEP zonunda MEP işlerine en erken hangi cephe/MEP sıralamasıyla başlanır?

- **Option 1, yapısal öncelikli:** L1 döşemesi → kalıp sökümü → 1,40 m dolgu → SoG → **blok duvar → sekonder çelik + kaplama** (seri) → MEP.
- **Option 2, cephe öncelikli:** L1 döşemesi kürlendikten sonra **duvarsız sekonder çelik + kaplama** yapılır. Bu iş dolgu/SoG zinciriyle **paralel** yürür.

## 2. Bu oturumda gelen girdiler

| Dosya | Not |
|---|---|
| `MEP_Start_Scenario_1n2_rev00_20260930.mpp` | Başlangıç programı |
| `05_Critical_MEP_Zone_and_Sequencing_Strategy.md` | Strateji notu (REV.11). Hâlâ eski zonu gösteriyor, bkz. §6 |
| `06_Facade_MEP_Sequencing_Comparison.xlsx` | Metraj, verim ve karşılaştırma tablosu. Hâlâ eski zon |
| RIBA 2 planları `UK207-100-A1-AP00-12001` (Basement), `-13001` (GF), `-14001` (L1), `-14501` (L2), `-17001` (Roof), `-18001` (Gantry) | Kritik zonun yeniden tanımı bunlara dayanıyor |

Bu dosyalar repoda **yok**. Yalnızca bu oturuma yüklendi.

## 3. Repodaki çıktılar

| Dosya | İçerik |
|---|---|
| `MEP_Start_Scenario_1n2_rev01_20260930.xml` | rev00 + 2 mantık düzeltmesi |
| `MEP_Start_Scenario_1n2_rev02_20260930.xml` | **Güncel sürüm.** Yeni kritik zon, radye, L1 kaideleri, ofis bodrumu |
| `scripts/uk207_build_rev02.py` | rev00 .mpp'den rev01 ve rev02'yi birebir yeniden üretir (MPXJ). Kullanım: `python3 scripts/uk207_build_rev02.py <rev00.mpp> <out_dir>`. Gereken: `pip install mpxj JPype1`, Java 11+ |

XML dosyaları MS Project XML formatında (MSPDI). MS Project'te açıp **Farklı Kaydet → .mpp** ile kaydedin. MPXJ .mpp yazamıyor.

## 4. Revizyonlar

### rev01: mantık düzeltmeleri
1. Option 1, "MEP START — Level 1": 1 günlük işti, 0 günlük milestone yapıldı. Option 2 ile tutarlı hale geldi.
2. Option 1, TWC ataması: F10'a bağlantısı `FS` idi, `SS` yapıldı. Option 2 ve tablodaki CDM-040 ile eşleşiyor. Kritik yolda değil.

### rev02: kritik zon, temel ve bodrum
1. **rev00'daki yapı hatası düzeltildi.** Option 2 özet satırı Option 1'in altına girinti almıştı, kardeş satır yapıldı. Eski "Option 1 = 99 gün" özeti bu yüzden yanlıştı.
2. **Kritik zon yeniden tanımlandı** (bkz. §5).
3. **Metraja bağlı süreler yeniden hesaplandı.** Tablodaki verimler değiştirilmedi, ROUNDUP uygulandı.

   | Aktivite | Formül | Eski | Yeni |
   |---|---|---|---|
   | Driven piles | 35 kazık / 8 kazık/gün | 3g | 5g |
   | Pile cap rebar | 35 / 6 kazık/gün | 3g | 6g |
   | L1 soffit strike | 1.246 m² / 175 m²/gün | 4g | 8g |
   | 1,40 m fill | 1.744 m³ / 180 m³/gün | 5g | 10g |
   | SoG prep + pour | 1.246 m² / 120 m²/gün | 6g | 11g |
   | Blockwork wall (Opt 1) | 1.330 m² / 60 m²/gün | 9g | 23g |
   | Secondary steel + cladding | 1.330 m² / 45 m²/gün | 12g | 30g |

4. **Kritik zon radyesi** eklendi. Konumu: backfill'den sonra, zemin kat kolonlarından önce.
   Zincir: blinding & DPM (2g) → rebar (9g, 150 m²/gün varsayımı) → edge formwork (SS+2, 3g) → pour (2g) → cure (3g).
5. **L1 housekeeping pads (4g)** eklendi. L1 kürü bitince başlıyor, L1 MEP başlangıcı da buna bağlı. Sebebi: Phase 1 L1'de.
6. **Ofis bodrumu** eklendi: aks 11–13 / C'–G, −4,00 m, ~450 m². Kritik zonun **dışında**, paralel bir zincir. Sırası: iksa → kazı → kazık → test → grobeton → BS 8102 yalıtımı → radye → perdeler → dış yalıtım ve geri dolgu → GF döşemesi. Toplam 57 gün, 07.04.2027'de bitiyor. Kritik yolda değil.

## 5. Kritik zon: neden değişti

Eski tanım (§2'deki "aks 9–13") planlarla tutmuyor:
- **Aks 11–13 ofis bloğu.** Zeminde `OS-GF` mahalleri var, L2'de ofisler. Bodrum da bu bölgenin altında, içinde yangın pompası, su tankları ve public health odası var. MEP enerjilendirmesi açısından kritik değil.
- **Asıl MEP altyapısı Data Hall'ların kuzey ve güney bantlarında.** Zemin kat ve L1'de üst üste:
  - Kuzey: GF `DC-GF-56…63` ↔ L1 `DC-L1-53…61` (STS / Elektrik / RMU / TX / MMR / HDA / BMS / ICT).
  - Güney: GF `DC-GF-19…26` ↔ L1 `DC-L1-16…24`.
- **Substation yerleri:** **Substation Phase-1** L1'de, aks 1–2 / A–B (`DC-L1-44/45`). **Substation Phase-2** aynı noktada zemin katta (`DC-GF-47/48`).
- **Salonlar:** GF'de Data Hall-1 (216 kabin) ve Data Hall-2 (96 kabin). L1'de Data Hall-3 ve Data Hall-4 (her biri 216 kabin).

**Kullanıcının onayladığı yeni tanım:**
- **Phase 1 = Data Hall-3 ve 4 (L1).** Bu bir yedek varsayım, Basis of Design raporuyla doğrulanacak.
- **Zon:** Substation Phase-1 (aks 1–2 / A–B) + kuzey bandı (aks 1–11 / A–B) + güney bandı (aks 2–11 / F–G), GF ve L1.
- **Metraj:**
  - Taban alanı: (69,15 + 61,30) × 9,55 ≈ **1.246 m²/kat**.
  - Kazık: 6 m grid ile **35 adet**.
  - Cephe: (69,15 + 61,30 + 9,55) × 9,5 ≈ **1.330 m²** (GF + L1; kuzey, güney ve batı ucu).

## 6. Sonuç (rev02)

Çalışma takvimi MPP'deki takvim: 5 günlük hafta, İngiltere resmi tatilleri dahil. Gün 1 = 04.01.2027.

| Gösterge | Option 1 | Option 2 | Kazanç |
|---|---|---|---|
| **MEP start, Level 1 (Phase 1)** | 162. iş günü / 23.08.2027 | 103. iş günü / 01.06.2027 | **59 iş günü** |
| MEP start, Ground Floor | 162. iş günü / 23.08.2027 | 112. iş günü / 14.06.2027 | 50 iş günü |

Option 2'de L1 MEP başlangıcını **cephe (30g)** belirliyor. Kalıp sökümü 28.04'te, L1 kaideleri 22.04'te bitiyor, ikisi de daha önce.

## 7. Varsayımlar ve sınırlar

- Tüm süreler gösterge niteliğinde. Verimler tablodaki genel İngiltere verimleri, sahada ölçülmüş değil.
- **Tek ekip varsayımı.** Kuzey ve güney cepheleri iki ekiple paralel yürürse Option 2'de L1 MEP başlangıcı yaklaşık 3 hafta öne çekilir. Bu modellenmedi.
- **Sabit süreler ölçeklenmedi.** Kolonlar, L1 döşeme kalıbı, donatısı ve dökümü gibi sabit süreler yeni alana göre büyütülmedi. İki seçenekte ortak oldukları için aradaki fark değişmez, ama mutlak tarihler iyimser.
- **Kaynak dengelemesi yok.** Bodrum ve kritik zon arasında vinç ve beton ekibi paylaşımı dengelenmedi.
- **Radye + 1,40 m dolgu + SoG kesitini kullanıcı tarif etti.** Radye kazık başlıklarının üzerinde, dolgu ve SoG radyenin üstünde. Statik çizimlerle teyit edilmeli.
- **Kazıklar varsayım.** Çakma kazık (tip onaylanmadı), 6 m grid.

## 8. Açık işler / sonraki adımlar

1. **Basis of Design raporu.** Bu oturumda yükleme ulaşmadı. Gelince Phase 1'in Data Hall-3/4 olup olmadığını teyit et. Farklıysa §5'teki zonu ve metrajı güncelle, betiği yeniden çalıştır (`ZONE`, `DUR` ve metraj sabitleri).
2. **`05_...md` ve `06_...xlsx` rev02'ye uyarlanmadı.** İkisi de hâlâ aks 9–13 / ~609 m² / 500 m² cephe gösteriyor. Uyarlanması gerekenler:
   - `ZONE_LENGTH` / `ZONE_DEPTH` / `FACADE_AREA_ZONE` değerleri.
   - BoQ-01 mahal listesi.
   - Yeni raft ve bodrum aktiviteleri.
   - Comparison sekmesi.
3. İsteğe bağlı: iki cephe ekibi senaryosu ve sabit sürelerin alana göre ölçeklenmesi.
4. PR #1 taslak durumda. Birleştirme kararı kullanıcıda.
