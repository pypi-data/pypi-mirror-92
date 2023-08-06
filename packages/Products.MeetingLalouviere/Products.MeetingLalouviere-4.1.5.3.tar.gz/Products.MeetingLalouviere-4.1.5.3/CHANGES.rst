Products.MeetingLalouviere Changelog
====================================

The Products.MeetingCommunes version must be the same as the Products.PloneMeeting version

4.1.5.3 (2021-01-27)
--------------------

- Fix alderman access to validated items.
  [odelaere]


4.1.5.2 (2021-01-14)
--------------------

- Fix commission on 01/01/21
  [odelaere]


4.1.5.1 (2020-08-25)
--------------------

- Fix commission order.
  [odelaere]


4.1.5 (2020-08-21)
------------------

- Adapted code and tests regarding DX meetingcategory.
  [gbastien]
- Adapted templates regarding last changes in Products.PloneMeeting.
  [gbastien]


4.1.4.4 (2020-06-24)
--------------------

- Fix WF conditions.
  [odelaere]


4.1.4.3 (2020-06-24)
--------------------

- Display `groupsInCharge` on the item view : when field `MeetingItem.groupsInCharge` is used, from the proposingGroup when
  `MeetingConfig.includeGroupsInChargeDefinedOnProposingGroup=True` or from the category when
  `MeetingConfig.includeGroupsInChargeDefinedOnCategory=True`.
  Set `autoInclude=True` by default instead `False` for `MeetingItem.getGroupsInCharge`


4.1.4.2 (2020-06-09)
--------------------

- Added DecisionSuite on item views.
  [odelaere]


4.1.4.1 (2020-06-04)
--------------------

- Use the UID from prod for DEF instead of trying to find it.
  [odelaere]


4.1.4 (2020-06-04)
------------------

- Fix for DEF intranet.
  [odelaere]


4.1.3 (2020-06-03)
------------------

- Fixed mayGenerateFinanceAdvice.
  [duchenean]


4.1.2 (2020-06-03)
------------------

- Fix budget reviewers access.
  [odelaere]


4.1.1 (2020-05-27)
------------------

- Fix sendMailIfRelevant.
  [odelaere]


4.1.1rc3 (2020-05-08)
---------------------

- Fixed printing methods.
  [duchenean]


4.1.1rc2 (2020-04-29)
---------------------

- Fixed item reference method.
  [odelaere]
- updated migration script to patch new workflow and its adaptations properly.
  [odelaere]


4.1.1rc1 (2020-04-24)
---------------------
- upgrade La Louvière profile whith MeetingCommunes 4.1.x features.
  [odelaere]
