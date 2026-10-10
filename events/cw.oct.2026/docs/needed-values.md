# Values needed to create the remaining VLP objects

Fill in the blanks below, then tell me to go create the objects. Grouped by session; each
section lists only what's still missing (already-created objects are not repeated here).

## VKS Fast Track (template VCF91VKS-FastTrack-v5, pool currently on VCF522-Upgrade-VCF9.1-REV1)

### Lab definition (`classes/lab_yaml/lab.clearwater.vcf91vks.yaml`)

| Field            | Current value | Needed                                                                    | <br />                                        |
| ---------------- | ------------- | ------------------------------------------------------------------------- | :-------------------------------------------- |
| shortDescription | `leave empty` | one-line summary shown in the admin Lab list and the lab console Labs tab | <br />                                        |
| description      | `leave empty` | longer text shown on the Lab Content tab                                  | <br />                                        |
| enabled          | false         | false>\`                                                                  | `true` once ready for the class, else `false` |

### Class definition (`classes/class_yaml/class.clearwater.vks-fasttrack.yaml`)

| Field                           | Current value                       | Needed                                                              |
| ------------------------------- | ----------------------------------- | ------------------------------------------------------------------- |
| schedule.startDate              | `2026-10-06`                        | class start date                                                    |
| schedule.startTime              | `<START_TIME HH:MM>`                | class start time (event tz: America/New_York)                       |
| schedule.endDate                | `<END_DATE YYYY-MM-DD>`             | class end date                                                      |
| schedule.endTime                | `<END_TIME HH:MM>`                  | class end time                                                      |
| numberOfSeats                   | `<SEATS>`                           | seat count                                                          |
| owners[0]                       | `<OWNER_EMAIL>`                     | class owner's email                                                 |
| provisioning.preProvisionPeriod | `<PRE_PROVISION_PERIOD d.hh:mm:ss>` | how long before start to pre-provision, e.g. `1.00:00:00` for 1 day |

## VCF Upgrade Fast Track (VC80U3-to-VCF911-Upgrade-Clearwater-Rev2 / manual "vSphere-to-VVF-Upgrade", VCF522-Upgrade-VCF9.1-REV1 / manual "VCF5.2.x-to-VCF9.1.x")

### Manual projects — blocked on source files, not just values

Source for both is noted as "ScreenSteps Import" (not a zip upload like VKS). Needed:

| Item                          | Needed                                                                       |
| ----------------------------- | ---------------------------------------------------------------------------- |
| vSphere-to-VVF-Upgrade source | the ScreenSteps export file/link; where should it live under `lab.manuals/`? |
| VCF5.2.x-to-VCF9.1.x source   | the ScreenSteps export file/link; where should it live under `lab.manuals/`? |

No lab/class definitions exist yet for this session — once the manual projects (and a pool for
VC80U3, once its shadow finishes) are in place, this section will need the same fields as VKS above.

## VCF AIRI Fast Track (VCF91-AIRI-FastTrack-Rev4 / manual "AIRI Fast Track")

Blocked upstream: the template still doesn't appear in the CloudShadow API at all, i.e. it isn't
synced to the Clearwater clouds yet. Nothing else can start until that's resolved (outside VLP
admin — likely needs the template pushed to the eduprod catalogs).

| Item                   | Needed                                                                                    |
| ---------------------- | ----------------------------------------------------------------------------------------- |
| AIRI Fast Track source | the ScreenSteps export file/link; where should it live under `lab.manuals/`?              |
| Template sync          | who/how gets VCF91-AIRI-FastTrack-Rev4 synced into the 3 Clearwater cloud orgs' catalogs? |

Once that's resolved, this section will need the same manual/lab/class fields as the sections above.
